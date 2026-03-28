#!/usr/bin/env python3
"""
Skill Puller - Download skills from GitHub to remote VMs

Fast skill downloader using git sparse-checkout - only downloads the requested skill
folder without cloning the entire repository.

Usage:
    ./pull.py skill-name                    # Pull to default host
    ./pull.py skill1 skill2                 # Pull multiple skills
    ./pull.py skill-name --host kai         # Pull to specific host
    ./pull.py skill-name --force            # Force re-download
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Configuration
DEFAULT_HOST = "kai"
GITHUB_REPO = "https://github.com/Judeqiu/weagents-public.git"
REMOTE_SKILLS_PATH = "~/.openclaw/workspace/skills"
SKILLS_SUBDIR = "skills"


def run_ssh_command(host: str, command: str, check: bool = True) -> tuple[int, str, str]:
    """Run a command on remote host via SSH."""
    ssh_cmd = ["ssh", host, command]
    try:
        result = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            check=False
        )
        # Combine stdout and stderr for better error detection
        combined_output = result.stdout + result.stderr
        if check and result.returncode != 0:
            print(f"❌ SSH command failed")
            if result.stderr:
                print(f"   Error: {result.stderr}")
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        if check:
            print(f"❌ SSH error: {e}")
        return 1, "", str(e)


def check_git_installed(host: str) -> bool:
    """Check if git is installed on remote host."""
    code, _, _ = run_ssh_command(host, "which git", check=False)
    return code == 0


def install_git(host: str) -> bool:
    """Install git on remote host."""
    print(f"📦 Installing git on {host}...")
    code, _, stderr = run_ssh_command(
        host,
        "sudo apt-get update -qq && sudo apt-get install -y -qq git",
        check=False
    )
    if code == 0:
        print(f"✅ git installed successfully")
        return True
    else:
        print(f"❌ Failed to install git: {stderr}")
        return False


def ensure_remote_dir(host: str) -> bool:
    """Ensure the remote skills directory exists."""
    code, _, _ = run_ssh_command(
        host,
        f"mkdir -p {REMOTE_SKILLS_PATH}",
        check=False
    )
    return code == 0


def skill_exists(host: str, skill_name: str) -> bool:
    """Check if skill already exists on remote host."""
    code, _, _ = run_ssh_command(
        host,
        f"test -d {REMOTE_SKILLS_PATH}/{skill_name}",
        check=False
    )
    return code == 0


def remove_skill(host: str, skill_name: str) -> bool:
    """Remove existing skill from remote host."""
    print(f"🗑️  Removing existing skill: {skill_name}")
    code, _, _ = run_ssh_command(
        host,
        f"rm -rf {REMOTE_SKILLS_PATH}/{skill_name}",
        check=False
    )
    return code == 0


def pull_skill(host: str, skill_name: str) -> bool:
    """Pull a skill from GitHub using git sparse-checkout."""
    temp_dir = f"~/.cache/skill-puller-{skill_name}"
    target_dir = f"{REMOTE_SKILLS_PATH}/{skill_name}"
    
    print(f"⬇️  Downloading {skill_name} from GitHub...")
    print(f"   Repo: {GITHUB_REPO}")
    
    # Use git sparse-checkout to download only the skill folder
    commands = f"""
rm -rf {temp_dir}
mkdir -p {temp_dir}
cd {temp_dir}
git init -q
git remote add origin {GITHUB_REPO}
git config core.sparseCheckout true
echo "{SKILLS_SUBDIR}/{skill_name}/*" > .git/info/sparse-checkout
if ! git pull -q --depth=1 origin main 2>/dev/null && ! git pull -q --depth=1 origin master 2>/dev/null; then
    echo "ERROR: Failed to fetch from repository"
    rm -rf {temp_dir}
    exit 1
fi
# Move skill files to target
mkdir -p {REMOTE_SKILLS_PATH}
if [ -d "{SKILLS_SUBDIR}/{skill_name}" ]; then
    mv {SKILLS_SUBDIR}/{skill_name} {target_dir}
else
    echo "Skill not found in repository: {skill_name}"
    rm -rf {temp_dir}
    exit 1
fi
# Cleanup
rm -rf {temp_dir}
"""
    
    code, stdout, stderr = run_ssh_command(host, commands, check=False)
    
    # Combine outputs for error detection
    combined = stdout + stderr
    
    if code == 0:
        print(f"✅ Downloaded successfully")
        return True
    else:
        if "could not read Username" in combined or "could not read Password" in combined:
            print(f"❌ The repository appears to be PRIVATE.")
            print(f"   This tool requires a PUBLIC repository.")
            print(f"   Use skill-deployer instead for private repos.")
        elif "not found" in combined.lower() or "does not exist" in combined.lower():
            print(f"❌ Skill not found in repository: {skill_name}")
        elif combined.strip():
            print(f"❌ Download failed: {combined.strip()}")
        else:
            print(f"❌ Download failed (exit code: {code})")
            print(f"   Make sure the repository is PUBLIC and accessible")
        return False


def set_permissions(host: str, skill_name: str) -> bool:
    """Set executable permissions on scripts."""
    skill_dir = f"{REMOTE_SKILLS_PATH}/{skill_name}"
    
    # Make Python and shell scripts executable
    commands = [
        f"find {skill_dir} -name '*.py' -type f -exec chmod +x {{}} \\; 2>/dev/null",
        f"find {skill_dir} -name '*.sh' -type f -exec chmod +x {{}} \\; 2>/dev/null",
    ]
    
    for cmd in commands:
        run_ssh_command(host, cmd, check=False)
    
    return True


def verify_skill(host: str, skill_name: str) -> bool:
    """Verify the skill was pulled correctly."""
    skill_dir = f"{REMOTE_SKILLS_PATH}/{skill_name}"
    
    # Check if directory exists
    code, _, _ = run_ssh_command(
        host,
        f"test -d {skill_dir}",
        check=False
    )
    if code != 0:
        print(f"❌ Skill directory not found: {skill_dir}")
        return False
    
    # Check if SKILL.md exists
    code, _, _ = run_ssh_command(
        host,
        f"test -f {skill_dir}/SKILL.md",
        check=False
    )
    if code != 0:
        print(f"❌ SKILL.md not found in {skill_name}")
        return False
    
    # Get skill info
    code, stdout, _ = run_ssh_command(
        host,
        f"head -5 {skill_dir}/SKILL.md | grep -E '^name:|^description:'",
        check=False
    )
    
    print(f"✅ Verification passed")
    if stdout:
        print(f"   {stdout.strip()}")
    
    return True


def list_available_skills(host: str) -> list[str]:
    """List available skills from GitHub repository using git ls-tree."""
    print(f"📋 Fetching available skills from GitHub...")
    print(f"   Repo: {GITHUB_REPO}")
    
    # Ensure git is installed
    if not check_git_installed(host):
        print(f"⚠️  git not found on {host}, attempting to install...")
        if not install_git(host):
            print(f"❌ Cannot proceed without git")
            return []
    
    # Use git ls-remote to list tree of skills directory
    # We need to clone just enough to list the directory
    temp_dir = "~/.cache/skill-puller-temp"
    
    # Create temp repo and list skills using sparse checkout
    commands = f"""
rm -rf {temp_dir}
mkdir -p {temp_dir}
cd {temp_dir}
git init -q
git remote add origin {GITHUB_REPO}
git config core.sparseCheckout true
echo "{SKILLS_SUBDIR}/*" > .git/info/sparse-checkout
if ! git pull -q --depth=1 origin main 2>/dev/null && ! git pull -q --depth=1 origin master 2>/dev/null; then
    echo "ERROR: Failed to fetch from repository"
    echo "Make sure the repository is PUBLIC"
    rm -rf {temp_dir}
    exit 1
fi
ls -1 {SKILLS_SUBDIR}/
rm -rf {temp_dir}
"""
    
    code, stdout, stderr = run_ssh_command(host, commands, check=False)
    
    if code != 0:
        print(f"❌ Failed to fetch skill list")
        if "could not read Username" in stderr:
            print(f"   The repository appears to be PRIVATE.")
            print(f"   This tool requires a PUBLIC repository.")
            print(f"   Use skill-deployer instead for private repos.")
        else:
            print(f"   Error: {stderr}")
        return []
    
    # Parse directory names
    skills = [
        line.strip()
        for line in stdout.split("\n")
        if line.strip() and not line.strip().endswith('.md') and not line.strip().endswith('.txt')
    ]
    
    return skills


def pull_single_skill(host: str, skill_name: str, force: bool = False) -> bool:
    """Pull a single skill to the remote host."""
    print(f"\n{'='*60}")
    print(f"📦 Processing: {skill_name}")
    print(f"🎯 Target Host: {host}")
    print(f"{'='*60}")
    
    # Check if git is installed
    if not check_git_installed(host):
        print(f"⚠️  git not found on {host}, attempting to install...")
        if not install_git(host):
            print(f"❌ Cannot proceed without git")
            return False
    
    # Ensure remote directory exists
    if not ensure_remote_dir(host):
        print(f"❌ Failed to create remote directory")
        return False
    
    # Check if skill already exists
    if skill_exists(host, skill_name):
        if force:
            if not remove_skill(host, skill_name):
                print(f"❌ Failed to remove existing skill")
                return False
        else:
            print(f"⚠️  Skill already exists: {skill_name}")
            print(f"   Use --force to re-download")
            return True
    
    # Pull the skill
    if not pull_skill(host, skill_name):
        return False
    
    # Set permissions
    set_permissions(host, skill_name)
    
    # Verify
    if not verify_skill(host, skill_name):
        return False
    
    print(f"✅ Successfully pulled {skill_name} to {host}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Download skills from GitHub repository to this OpenClaw VM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
For OpenClaw Agents:
  ./pull.py SKILL_NAME            # Install a skill from GitHub
  ./pull.py --list                # See what skills are available
  ./pull.py SKILL_NAME --force    # Update/reinstall a skill

Examples:
  ./pull.py lextok-search
  ./pull.py lextok-search producthunter caddy-manager
  ./pull.py marketing-creator --force
        """
    )
    
    parser.add_argument(
        "skills",
        nargs="*",
        help="Skill name(s) to pull"
    )
    
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help=f"Target host (default: {DEFAULT_HOST})"
    )
    
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-download if skill exists"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available skills from GitHub"
    )
    
    args = parser.parse_args()
    
    # List available skills
    if args.list:
        skills = list_available_skills(args.host)
        if skills:
            print(f"\n📋 Available Skills ({len(skills)} total):")
            print(f"{'='*60}")
            for skill in sorted(skills):
                print(f"  • {skill}")
            print(f"{'='*60}")
            print(f"\nUse: ./pull.py <skill-name> to download")
        return
    
    # Validate skill names
    if not args.skills and not args.list:
        parser.print_help()
        print("\n❌ Error: No skill names provided")
        print("\n💡 For OpenClaw agents:")
        print("   1. To list available skills: ./pull.py --list")
        print("   2. To install a skill: ./pull.py SKILL_NAME")
        print("   3. Example: ./pull.py lextok-search")
        sys.exit(1)
    
    # Pull each skill
    print(f"🚀 Skill Puller - Download from GitHub")
    print(f"{'='*60}")
    print(f"📁 Repository: {GITHUB_REPO}")
    print(f"🎯 Host: {args.host}")
    
    success_count = 0
    fail_count = 0
    
    for skill_name in args.skills:
        if pull_single_skill(args.host, skill_name, args.force):
            success_count += 1
        else:
            fail_count += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 Summary")
    print(f"{'='*60}")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {fail_count}")
    print(f"   Host: {args.host}")
    print(f"   Path: {REMOTE_SKILLS_PATH}")
    
    if fail_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()

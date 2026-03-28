#!/usr/bin/env python3
"""
Skill Downloader - Download skills from remote VMs to local machine

Downloads skills FROM a remote OpenClaw VM TO your local ./skills/ folder.
Useful for backing up, editing, or redistributing skills.

Usage:
    ./download.py skill-name                    # Download from default host
    ./download.py skill1 skill2                 # Download multiple skills
    ./download.py skill-name --host kai         # Download from specific host
    ./download.py skill-name --output ./skills  # Custom output directory
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path

# Configuration
DEFAULT_HOST = "kai"
REMOTE_SKILLS_PATH = "~/.openclaw/workspace/skills"
LOCAL_SKILLS_PATH = "./skills"


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
        if check and result.returncode != 0:
            print(f"❌ SSH command failed")
            if result.stderr:
                print(f"   Error: {result.stderr}")
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        if check:
            print(f"❌ SSH error: {e}")
        return 1, "", str(e)


def check_skill_exists_on_remote(host: str, skill_name: str) -> bool:
    """Check if skill exists on remote host."""
    code, _, _ = run_ssh_command(
        host,
        f"test -d {REMOTE_SKILLS_PATH}/{skill_name}",
        check=False
    )
    return code == 0


def list_remote_skills(host: str) -> list[str]:
    """List all skills available on remote host."""
    code, stdout, stderr = run_ssh_command(
        host,
        f"ls -1 {REMOTE_SKILLS_PATH}/",
        check=False
    )
    if code != 0:
        print(f"❌ Failed to list remote skills: {stderr}")
        return []
    
    skills = [line.strip() for line in stdout.split("\n") if line.strip()]
    return skills


def download_skill(host: str, skill_name: str, output_dir: str) -> bool:
    """Download a skill from remote host using tar over SSH."""
    remote_path = f"{REMOTE_SKILLS_PATH}/{skill_name}"
    local_path = os.path.join(output_dir, skill_name)
    
    # Check if exists locally
    if os.path.exists(local_path):
        print(f"⚠️  Skill already exists locally: {local_path}")
        return False, "exists"
    
    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"⬇️  Downloading {skill_name} from {host}...")
    
    # Use tar to archive, stream via SSH, and extract locally
    # This preserves file permissions and handles all file types
    try:
        # Create tar archive on remote and stream to local
        tar_cmd = f"tar -czf - -C {REMOTE_SKILLS_PATH} {skill_name}"
        ssh_cmd = ["ssh", host, tar_cmd]
        
        # Run SSH and capture the tar stream
        ssh_process = subprocess.Popen(
            ssh_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Extract tar stream to output directory
        extract_cmd = ["tar", "-xzf", "-", "-C", output_dir]
        extract_process = subprocess.Popen(
            extract_cmd,
            stdin=ssh_process.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Close stdout to allow SSH to receive SIGPIPE if extract fails
        ssh_process.stdout.close()
        
        # Wait for both processes
        extract_stdout, extract_stderr = extract_process.communicate()
        ssh_stdout, ssh_stderr = ssh_process.communicate()
        
        # Check results
        if ssh_process.returncode != 0:
            print(f"❌ SSH failed: {ssh_stderr.decode()}")
            return False, "ssh_error"
        
        if extract_process.returncode != 0:
            print(f"❌ Extract failed: {extract_stderr.decode()}")
            return False, "extract_error"
        
        print(f"✅ Downloaded successfully to {local_path}")
        return True, "success"
        
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False, "exception"


def verify_local_skill(skill_name: str, output_dir: str) -> bool:
    """Verify the skill was downloaded correctly."""
    skill_path = os.path.join(output_dir, skill_name)
    
    # Check if directory exists
    if not os.path.isdir(skill_path):
        print(f"❌ Skill directory not found: {skill_path}")
        return False
    
    # Check if SKILL.md exists
    skill_md = os.path.join(skill_path, "SKILL.md")
    if not os.path.isfile(skill_md):
        print(f"❌ SKILL.md not found in {skill_name}")
        return False
    
    # Count files
    try:
        file_count = len([f for f in os.listdir(skill_path) if os.path.isfile(os.path.join(skill_path, f))])
        print(f"✅ Verification passed ({file_count} files)")
        return True
    except:
        print(f"✅ Verification passed")
        return True


def download_single_skill(host: str, skill_name: str, output_dir: str, force: bool = False) -> bool:
    """Download a single skill from remote to local."""
    print(f"\n{'='*60}")
    print(f"📦 Processing: {skill_name}")
    print(f"🎯 Source: {host}")
    print(f"📁 Destination: {output_dir}")
    print(f"{'='*60}")
    
    # Check if skill exists on remote
    if not check_skill_exists_on_remote(host, skill_name):
        print(f"❌ Skill not found on remote host: {skill_name}")
        print(f"   Check available skills: ssh {host} \"ls {REMOTE_SKILLS_PATH}/\"")
        return False
    
    # Check if exists locally
    local_path = os.path.join(output_dir, skill_name)
    if os.path.exists(local_path):
        if force:
            print(f"🗑️  Removing existing local skill: {local_path}")
            import shutil
            shutil.rmtree(local_path)
        else:
            print(f"⚠️  Skill already exists locally: {local_path}")
            print(f"   Use --force to overwrite")
            return True
    
    # Download the skill
    success, status = download_skill(host, skill_name, output_dir)
    
    if not success:
        return status == "exists"  # Return True if it was just "already exists"
    
    # Verify
    if not verify_local_skill(skill_name, output_dir):
        return False
    
    print(f"✅ Successfully downloaded {skill_name}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Download skills from remote VMs to local machine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ./download.py lextok-search                  # Download from default host
  ./download.py lextok-search producthunter    # Download multiple skills
  ./download.py marketing-creator --host enraie # Download from specific host
  ./download.py lextok-search --output ./my-skills/  # Custom output directory
  ./download.py lextok-search --force          # Overwrite existing

List remote skills:
  ssh kai "ls ~/.openclaw/workspace/skills/"
        """
    )
    
    parser.add_argument(
        "skills",
        nargs="*",
        help="Skill name(s) to download"
    )
    
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help=f"Source host (default: {DEFAULT_HOST})"
    )
    
    parser.add_argument(
        "--output",
        default=LOCAL_SKILLS_PATH,
        help=f"Output directory (default: {LOCAL_SKILLS_PATH})"
    )
    
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing local skill"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available skills on remote host"
    )
    
    args = parser.parse_args()
    
    # List remote skills
    if args.list:
        print(f"📋 Listing skills on {args.host}...")
        skills = list_remote_skills(args.host)
        if skills:
            print(f"\n📋 Available Skills ({len(skills)} total):")
            print(f"{'='*60}")
            for skill in sorted(skills):
                print(f"  • {skill}")
            print(f"{'='*60}")
            print(f"\nUse: ./download.py <skill-name> to download")
        else:
            print("❌ No skills found or connection failed")
        return
    
    # Validate skill names
    if not args.skills:
        parser.print_help()
        print("\n❌ Error: No skill names provided")
        print("\n💡 To see available skills:")
        print(f"   ./download.py --list")
        print(f"   or: ssh {args.host} 'ls {REMOTE_SKILLS_PATH}/'")
        sys.exit(1)
    
    # Convert output path to absolute
    output_dir = os.path.abspath(os.path.expanduser(args.output))
    
    # Download each skill
    print(f"🚀 Skill Downloader - VM to Local")
    print(f"{'='*60}")
    print(f"🎯 Source Host: {args.host}")
    print(f"📁 Output Directory: {output_dir}")
    
    success_count = 0
    fail_count = 0
    skip_count = 0
    
    for skill_name in args.skills:
        result = download_single_skill(args.host, skill_name, output_dir, args.force)
        if result:
            success_count += 1
        else:
            fail_count += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 Summary")
    print(f"{'='*60}")
    print(f"✅ Downloaded: {success_count}")
    print(f"⏭️  Skipped (exists): {skip_count}")
    print(f"❌ Failed: {fail_count}")
    print(f"   Source: {args.host}")
    print(f"   Output: {output_dir}")
    
    if fail_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()

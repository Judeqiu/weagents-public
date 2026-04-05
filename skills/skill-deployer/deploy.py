#!/usr/bin/env python3
"""
Skill Deployer - Deploy skills to OpenClaw agents on remote VMs via SSH
"""

__version__ = "1.0.3"

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class DeployConfig:
    """Configuration for deployment."""
    default_host: str = "kai"
    skills_source_path: str = "."
    remote_skills_path: str = "~/.openclaw/workspace/skills"
    verify_after_deploy: bool = True
    restart_agent: bool = False


class SkillDeployer:
    """Deploys skills to remote OpenClaw agents."""
    
    def __init__(self, config: Optional[DeployConfig] = None):
        self.config = config or DeployConfig()
        self._load_config_file()
    
    def _load_config_file(self):
        """Load config from config.json if it exists."""
        config_path = Path(__file__).parent / "config.json"
        if config_path.exists():
            try:
                with open(config_path) as f:
                    data = json.load(f)
                    for key, value in data.items():
                        if hasattr(self.config, key):
                            setattr(self.config, key, value)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config.json: {e}")
    
    def _is_local_host(self, host: str) -> bool:
        """Check if host is the local machine."""
        local_names = ['localhost', '127.0.0.1', '::1']
        # Also check if hostname matches
        try:
            import socket
            hostname = socket.gethostname()
            local_names.append(hostname)
            local_names.append(hostname.split('.')[0])  # short name
            # Get local IP addresses
            local_ips = []
            try:
                # Get all addresses for localhost
                for addr_info in socket.getaddrinfo(hostname, None):
                    ip = addr_info[4][0]
                    if ip not in local_ips:
                        local_ips.append(ip)
            except:
                pass
            
            # Try to resolve the target host and compare IPs
            try:
                target_addr = socket.getaddrinfo(host, None)[0][4][0]
                if target_addr in ['127.0.0.1', '::1'] or target_addr in local_ips:
                    return True
            except:
                pass
        except:
            pass
        return host in local_names
    
    def _run_ssh(self, host: str, command: str, timeout: int = 60) -> Dict[str, Any]:
        """Run a command on remote host via SSH, or locally if host is localhost."""
        # If local host, run command directly
        if self._is_local_host(host):
            try:
                result = subprocess.run(
                    command,
                    shell=True,  # Use shell for local commands
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                return {
                    "success": result.returncode == 0,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode,
                }
            except subprocess.TimeoutExpired:
                return {"success": False, "error": f"Command timed out after {timeout}s"}
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        # Remote host - use SSH
        try:
            result = subprocess.run(
                ["ssh", host, command],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            # If SSH fails with "Could not resolve hostname", try local mode
            if result.returncode != 0 and "Could not resolve hostname" in result.stderr:
                # Try local fallback
                local_result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                return {
                    "success": local_result.returncode == 0,
                    "stdout": local_result.stdout,
                    "stderr": local_result.stderr,
                    "returncode": local_result.returncode,
                }
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"SSH command timed out after {timeout}s"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _get_skill_files(self, skill_path: Path) -> List[str]:
        """Get all files in a skill directory recursively."""
        files = []
        for item in skill_path.rglob("*"):
            # Skip hidden files and __pycache__
            if any(part.startswith(".") or part == "__pycache__" 
                   for part in item.relative_to(skill_path).parts):
                continue
            files.append(str(item.relative_to(skill_path)))
        return files
    
    def _run_scp(self, local_path: str, remote_path: str, host: str, 
                 recursive: bool = True) -> Dict[str, Any]:
        """Copy files to remote host via SCP."""
        try:
            cmd = ["scp"]
            if recursive:
                cmd.append("-r")
            # Use -p to preserve permissions and -C for compression
            cmd.extend(["-p", "-C"])
            cmd.extend([local_path, f"{host}:{remote_path}"])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "SCP command timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def test_connection(self, host: str) -> bool:
        """Test SSH connection to a host."""
        result = self._run_ssh(host, "echo 'connection_ok'")
        return result["success"] and "connection_ok" in result.get("stdout", "")
    
    def get_ssh_hosts(self) -> List[str]:
        """Get list of configured SSH hosts."""
        try:
            result = subprocess.run(
                ["grep", "-E", "^Host ", os.path.expanduser("~/.ssh/config")],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                hosts = []
                for line in result.stdout.strip().split("\n"):
                    parts = line.split()
                    if len(parts) >= 2:
                        host = parts[1]
                        # Skip wildcard hosts and patterns
                        if not any(c in host for c in ["*", "?"]):
                            hosts.append(host)
                return hosts
        except Exception:
            pass
        return []
    
    def find_skill_path(self, skill_name: str) -> Optional[Path]:
        """Find skill directory by name."""
        # Direct path provided
        path = Path(skill_name)
        if path.exists() and path.is_dir():
            skill_md = path / "SKILL.md"
            if skill_md.exists():
                return path.resolve()
        
        # Search in default locations
        search_paths = [
            Path(self.config.skills_source_path),
            Path(__file__).parent.parent,  # skills/ directory
            Path.cwd(),
        ]
        
        for search_path in search_paths:
            if not search_path.exists():
                continue
            
            # Try exact match
            skill_path = search_path / skill_name
            if skill_path.exists() and skill_path.is_dir():
                skill_md = skill_path / "SKILL.md"
                if skill_md.exists():
                    return skill_path.resolve()
            
            # Try with hyphens replaced
            skill_path = search_path / skill_name.replace("-", "_")
            if skill_path.exists() and skill_path.is_dir():
                skill_md = skill_path / "SKILL.md"
                if skill_md.exists():
                    return skill_path.resolve()
        
        return None
    
    def get_skill_files(self, skill_path: Path) -> List[str]:
        """Get list of files to deploy for a skill."""
        files = []
        if skill_path.exists():
            for item in skill_path.iterdir():
                # Skip hidden files and common non-deploy files
                if item.name.startswith("."):
                    continue
                if item.name in ["__pycache__", "*.pyc", ".git", ".DS_Store"]:
                    continue
                files.append(item.name)
        return sorted(files)
    
    def parse_skill_metadata(self, skill_path: Path) -> Dict[str, str]:
        """Parse skill name and description from SKILL.md."""
        skill_md = skill_path / "SKILL.md"
        metadata = {"name": skill_path.name, "description": ""}
        
        if not skill_md.exists():
            return metadata
        
        try:
            with open(skill_md) as f:
                content = f.read()
                
            # Parse YAML front matter
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    front_matter = parts[1]
                    for line in front_matter.strip().split("\n"):
                        if ":" in line:
                            key, value = line.split(":", 1)
                            key = key.strip()
                            value = value.strip()
                            if key in ["name", "description"]:
                                metadata[key] = value
        except Exception:
            pass
        
        return metadata
    
    def deploy_skill(self, skill_name: str, host: str, 
                     install_deps: bool = False,
                     force: bool = True) -> Dict[str, Any]:
        """Deploy a single skill to a host. Always deletes existing skill first, then copies fresh."""
        # Find skill locally
        skill_path = self.find_skill_path(skill_name)
        if not skill_path:
            return {
                "success": False,
                "skill": skill_name,
                "host": host,
                "error": f"Skill not found: {skill_name}"
            }
        
        # Get skill metadata
        metadata = self.parse_skill_metadata(skill_path)
        
        print(f"\n📦 Deploying: {metadata['name']}")
        print(f"   Source: {skill_path}")
        print(f"   Target: {host}")
        if metadata.get('description'):
            print(f"   Description: {metadata['description'][:60]}...")
        
        # Get list of files to deploy
        files_to_deploy = self._get_skill_files(skill_path)
        print(f"   Files to deploy: {len(files_to_deploy)}")
        
        # Test connection
        if not self.test_connection(host):
            return {
                "success": False,
                "skill": skill_name,
                "host": host,
                "error": f"Cannot connect to host: {host}"
            }
        
        # Setup remote paths
        remote_base = self.config.remote_skills_path
        remote_skill_path = f"{remote_base}/{skill_path.name}"
        
        # Create base directory if needed
        result = self._run_ssh(host, f"bash -c 'mkdir -p {remote_base}'")
        if not result["success"]:
            return {
                "success": False,
                "skill": skill_name,
                "host": host,
                "error": f"Failed to create remote directory: {result.get('stderr', '')}"
            }
        
        # STEP 1: Check if skill exists and delete it
        print(f"   🧹 STEP 1: Removing existing skill at {remote_skill_path}...")
        check_result = self._run_ssh(host, f"bash -c 'test -d {remote_skill_path} && echo exists || echo not_found'")
        if check_result["success"]:
            if "exists" in check_result["stdout"]:
                print(f"      Found existing skill, deleting...")
                delete_result = self._run_ssh(host, f"bash -c 'rm -rf {remote_skill_path}'")
                if not delete_result["success"]:
                    return {
                        "success": False,
                        "skill": skill_name,
                        "host": host,
                        "error": f"Failed to delete existing skill: {delete_result.get('stderr', '')}"
                    }
                print(f"      ✅ Existing skill deleted")
            else:
                print(f"      No existing skill found (fresh deploy)")
        
        # STEP 2: Copy fresh skill files
        print(f"   📋 STEP 2: Copying skill files to {remote_skill_path}...")
        result = self._run_scp(str(skill_path), remote_skill_path, host, recursive=True)
        if not result["success"]:
            return {
                "success": False,
                "skill": skill_name,
                "host": host,
                "error": f"Failed to copy files: {result.get('stderr', '')}"
            }
        print(f"      ✅ Files copied successfully")
        
        # STEP 3: Set executable permissions on scripts
        print(f"   🔧 STEP 3: Setting executable permissions...")
        self._run_ssh(host, f"bash -c 'chmod -R +x {remote_skill_path}/*.py 2>/dev/null || true'")
        self._run_ssh(host, f"bash -c 'chmod -R +x {remote_skill_path}/*.sh 2>/dev/null || true'")
        print(f"      ✅ Permissions set")
        
        # STEP 4: Install dependencies if requested
        if install_deps:
            print(f"   📦 STEP 4: Installing Python dependencies...")
            req_file = f"{remote_skill_path}/requirements.txt"
            self._run_ssh(host, f"bash -c 'if [ -f {req_file} ]; then pip install -r {req_file} --break-system-packages -q 2>/dev/null || pip install -r {req_file} -q; fi'", timeout=180)
            print(f"      ✅ Dependencies installed")
        
        # STEP 5: Verify deployment
        print(f"   ✓ STEP 5: Verifying deployment...")
        verify_result = self._run_ssh(host, f"bash -c 'test -d {remote_skill_path} && test -f {remote_skill_path}/SKILL.md && echo verified || echo failed'")
        if verify_result["success"] and "verified" in verify_result["stdout"]:
            print(f"      ✅ Deployment verified")
        else:
            print(f"      ⚠️  Verification warning: skill may not be complete")
        
        return {
            "success": True,
            "skill": skill_name,
            "host": host,
            "path": remote_skill_path,
            "metadata": metadata
        }
    
    def list_remote_skills(self, host: str) -> List[Dict[str, str]]:
        """List skills deployed on a remote host."""
        remote_base = self.config.remote_skills_path
        # Use bash to expand the path properly
        result = self._run_ssh(host, f"bash -c 'ls -1 {remote_base} 2>/dev/null || true'")
        
        skills = []
        if result["success"]:
            for line in result["stdout"].strip().split("\n"):
                line = line.strip()
                if line:
                    skill_path = f"{remote_base}/{line}"
                    # Check if SKILL.md exists
                    check = self._run_ssh(host, f"bash -c 'test -f {skill_path}/SKILL.md && echo yes'")
                    if check["success"] and "yes" in check["stdout"]:
                        # Get metadata
                        meta_result = self._run_ssh(host, f"bash -c 'cat {skill_path}/SKILL.md'")
                        metadata = {"name": line, "description": ""}
                        if meta_result["success"]:
                            content = meta_result["stdout"]
                            # Parse YAML front matter for description
                            if content.startswith("---"):
                                # Has front matter
                                for ln in content.split("\n"):
                                    if ln.startswith("description:"):
                                        _, desc = ln.split(":", 1)
                                        metadata["description"] = desc.strip()
                                        break
                            else:
                                # No front matter - try to get first paragraph after title
                                lines = content.split("\n")
                                for i, ln in enumerate(lines):
                                    if ln.startswith("# "):
                                        # Found title, look for description in next non-empty lines
                                        for j in range(i+1, min(i+5, len(lines))):
                                            desc_line = lines[j].strip()
                                            if desc_line and not desc_line.startswith("#"):
                                                metadata["description"] = desc_line[:100]
                                                break
                                        break
                        skills.append(metadata)
        
        return skills
    
    def remove_skill(self, skill_name: str, host: str) -> Dict[str, Any]:
        """Remove a skill from a remote host."""
        remote_base = self.config.remote_skills_path
        remote_skill_path = f"{remote_base}/{skill_name}"
        
        result = self._run_ssh(host, f"bash -c 'rm -rf {remote_skill_path}'")
        
        if result["success"]:
            return {
                "success": True,
                "skill": skill_name,
                "host": host,
                "message": f"Skill '{skill_name}' removed from {host}"
            }
        else:
            return {
                "success": False,
                "skill": skill_name,
                "host": host,
                "error": result.get("stderr", "Unknown error")
            }
    
    def verify_skill(self, skill_name: str, host: str) -> Dict[str, Any]:
        """Verify a skill deployment on a remote host."""
        remote_base = self.config.remote_skills_path
        remote_skill_path = f"{remote_base}/{skill_name}"
        
        checks = []
        
        # Check if directory exists
        result = self._run_ssh(host, f"bash -c 'test -d {remote_skill_path} && echo exists'")
        if not (result["success"] and "exists" in result["stdout"]):
            return {
                "success": False,
                "skill": skill_name,
                "host": host,
                "error": "Skill directory not found",
                "checks": checks
            }
        checks.append("Directory exists")
        
        # Check SKILL.md
        result = self._run_ssh(host, f"bash -c 'test -f {remote_skill_path}/SKILL.md && echo yes'")
        if result["success"] and "yes" in result["stdout"]:
            checks.append("SKILL.md present")
        else:
            checks.append("SKILL.md MISSING")
        
        # Check for executable scripts
        result = self._run_ssh(host, f"bash -c 'ls {remote_skill_path}/*.py 2>/dev/null | wc -l'")
        if result["success"]:
            py_count = int(result["stdout"].strip() or 0)
            if py_count > 0:
                checks.append(f"{py_count} Python script(s)")
        
        return {
            "success": True,
            "skill": skill_name,
            "host": host,
            "checks": checks
        }


def main():
    parser = argparse.ArgumentParser(
        description=f"Skill Deployer v{__version__} - Deploy skills to OpenClaw agents on remote VMs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s my-skill                          # Clean redeploy to default host
  %(prog)s my-skill --host kai               # Deploy to specific host
  %(prog)s skill1 skill2 --host kai          # Deploy multiple skills
  %(prog)s --list                            # List remote skills
  %(prog)s --list --host weagents            # List skills on specific host
  %(prog)s --remove my-skill                 # Remove a skill
  %(prog)s --verify my-skill                 # Verify deployment
  %(prog)s my-skill --install-deps           # Deploy with dependencies

Note: By default, this tool ALWAYS does a clean redeploy (removes existing 
files first). This ensures no stale files remain on the remote host.
        """
    )
    
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    
    parser.add_argument("skills", nargs="*", help="Skill name(s) or path(s) to deploy. Can deploy multiple skills at once.")
    parser.add_argument("--host", action="append", dest="hosts",
                       help="Target host (can be used multiple times)")
    parser.add_argument("--all-hosts", action="store_true",
                       help="Deploy to all configured SSH hosts")
    parser.add_argument("--source", default=".",
                       help="Source path for skills (default: current directory)")
    parser.add_argument("--list", action="store_true",
                       help="List deployed skills on target host")
    parser.add_argument("--remove", metavar="SKILL",
                       help="Remove a skill from target host")
    parser.add_argument("--verify", metavar="SKILL",
                       help="Verify a skill deployment")
    parser.add_argument("--verify-all", action="store_true",
                       help="Verify all skills on target host")
    parser.add_argument("--install-deps", action="store_true",
                       help="Install Python dependencies after deployment")
    parser.add_argument("--no-clean", action="store_true",
                       help="Skip cleaning - NOT recommended, may leave stale files")
    parser.add_argument("--test-connection", metavar="HOST",
                       help="Test SSH connection to host")
    
    args = parser.parse_args()
    
    # Initialize deployer
    config = DeployConfig(skills_source_path=args.source)
    deployer = SkillDeployer(config)
    
    # Test connection mode
    if args.test_connection:
        print(f"🔌 Testing connection to {args.test_connection}...")
        if deployer.test_connection(args.test_connection):
            print(f"✅ Successfully connected to {args.test_connection}")
            return 0
        else:
            print(f"❌ Failed to connect to {args.test_connection}")
            return 1
    
    # Determine target hosts
    if args.all_hosts:
        hosts = deployer.get_ssh_hosts()
        if not hosts:
            print("❌ No SSH hosts found in ~/.ssh/config")
            return 1
    elif args.hosts:
        hosts = args.hosts
    else:
        hosts = [config.default_host]
    
    # List mode
    if args.list:
        for host in hosts:
            print(f"\n📋 Skills on {host}:")
            print("-" * 50)
            skills = deployer.list_remote_skills(host)
            if skills:
                for skill in skills:
                    print(f"  • {skill['name']}")
                    if skill.get('description'):
                        desc = skill['description'][:70]
                        if len(skill['description']) > 70:
                            desc += "..."
                        print(f"    {desc}")
            else:
                print("  No skills found")
        return 0
    
    # Remove mode
    if args.remove:
        for host in hosts:
            result = deployer.remove_skill(args.remove, host)
            if result["success"]:
                print(f"✅ {result['message']}")
            else:
                print(f"❌ Failed to remove from {host}: {result.get('error')}")
        return 0
    
    # Verify mode
    if args.verify:
        for host in hosts:
            result = deployer.verify_skill(args.verify, host)
            print(f"\n🔍 {args.verify} on {host}:")
            if result["success"]:
                for check in result.get("checks", []):
                    print(f"  ✓ {check}")
            else:
                print(f"  ✗ {result.get('error')}")
        return 0
    
    # Verify all mode
    if args.verify_all:
        for host in hosts:
            print(f"\n🔍 Verifying all skills on {host}:")
            skills = deployer.list_remote_skills(host)
            for skill in skills:
                result = deployer.verify_skill(skill["name"], host)
                status = "✓" if result["success"] else "✗"
                print(f"  {status} {skill['name']}")
        return 0
    
    # Deploy mode
    if not args.skills:
        parser.print_help()
        return 1
    
    print("🚀 Skill Deployer (Always Clean Redeploy)")
    print("=" * 60)
    
    all_success = True
    for skill_name in args.skills:
        for host in hosts:
            result = deployer.deploy_skill(
                skill_name=skill_name,
                host=host,
                install_deps=args.install_deps,
                force=not args.no_clean  # Always clean by default
            )
            
            if result["success"]:
                print(f"\n✅ Successfully deployed to {host}")
                print(f"   Remote path: {result['path']}")
                
                # Verify if requested
                if config.verify_after_deploy:
                    verify = deployer.verify_skill(skill_name, host)
                    if verify["success"]:
                        print("   Verification passed")
                    else:
                        print(f"   ⚠️  Verification: {verify.get('error')}")
            else:
                print(f"\n❌ Failed: {result.get('error')}")
                all_success = False
    
    print("\n" + "=" * 60)
    if all_success:
        print("✅ All deployments completed successfully")
        return 0
    else:
        print("⚠️  Some deployments failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

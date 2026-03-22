#!/usr/bin/env python3
"""
Deploy marketing-creator skill to remote host (kai) via SSH/SCP
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import Optional, Dict, Any, List


class Deployer:
    """Deploys marketing-creator skill to remote host."""
    
    DEFAULT_HOST = "kai"
    DEFAULT_USER = "ubuntu"
    REMOTE_PATH = "/home/ubuntu/.config/agents/skills/marketing-creator"
    
    # Files to deploy
    FILES_TO_DEPLOY = [
        "SKILL.md",
        "marketing.py",
        "byteplus_client.py",
        "model_selector.py",
        "telegram_poster.py",
        "api_reference.py",
        "test_setup.py",
        "requirements.txt",
        "config.json",
        "install.sh",
    ]
    
    def __init__(self, host: str = DEFAULT_HOST, user: str = DEFAULT_USER):
        self.host = host
        self.user = user
        self.remote_path = self.REMOTE_PATH
        self.local_path = Path(__file__).parent
    
    def _run_ssh(self, command: str, timeout: int = 60) -> Dict[str, Any]:
        """Run command on remote host via SSH."""
        ssh_cmd = ["ssh", f"{self.host}", command]
        try:
            result = subprocess.run(
                ssh_cmd,
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
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _run_scp(self, local_file: str, remote_file: str) -> Dict[str, Any]:
        """Copy file to remote host via SCP."""
        cmd = ["scp", local_file, f"{self.host}:{remote_file}"]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def check_connection(self) -> bool:
        """Check SSH connection to host."""
        result = self._run_ssh("echo 'connected'")
        return result["success"] and "connected" in result["stdout"]
    
    def create_remote_directory(self) -> bool:
        """Create remote directory structure."""
        result = self._run_ssh(f"mkdir -p {self.remote_path}")
        return result["success"]
    
    def deploy_file(self, filename: str) -> Dict[str, Any]:
        """Deploy a single file to remote host."""
        local_file = self.local_path / filename
        remote_file = f"{self.remote_path}/{filename}"
        
        if not local_file.exists():
            return {
                "success": False,
                "filename": filename,
                "error": f"Local file not found: {local_file}"
            }
        
        result = self._run_scp(str(local_file), remote_file)
        return {
            "success": result["success"],
            "filename": filename,
            "error": result.get("stderr") if not result["success"] else None
        }
    
    def deploy_all(self) -> Dict[str, Any]:
        """Deploy all files to remote host."""
        print(f"🚀 Deploying marketing-creator to {self.host}")
        print("=" * 60)
        
        # Check connection
        print("\n1️⃣ Checking SSH connection...")
        if not self.check_connection():
            print(f"❌ Failed to connect to {self.host}")
            print("   Make sure the host is configured in ~/.ssh/config")
            return {"success": False, "error": "SSH connection failed"}
        print(f"✅ Connected to {self.host}")
        
        # Create remote directory
        print("\n2️⃣ Creating remote directory structure...")
        if not self.create_remote_directory():
            print(f"❌ Failed to create remote directory")
            return {"success": False, "error": "Directory creation failed"}
        print(f"✅ Remote directory ready: {self.remote_path}")
        
        # Deploy files
        print("\n3️⃣ Deploying files...")
        deployed = []
        failed = []
        
        for filename in self.FILES_TO_DEPLOY:
            result = self.deploy_file(filename)
            if result["success"]:
                print(f"   ✅ {filename}")
                deployed.append(filename)
            else:
                print(f"   ❌ {filename}: {result.get('error', 'Unknown error')}")
                failed.append(filename)
        
        # Make scripts executable
        print("\n4️⃣ Setting executable permissions...")
        self._run_ssh(f"chmod +x {self.remote_path}/marketing.py")
        self._run_ssh(f"chmod +x {self.remote_path}/install.sh")
        self._run_ssh(f"chmod +x {self.remote_path}/deploy.py")
        print("   ✅ Permissions set")
        
        # Install dependencies on remote
        print("\n5️⃣ Installing dependencies on remote host...")
        result = self._run_ssh(
            f"cd {self.remote_path} && pip install -r requirements.txt -q",
            timeout=120
        )
        if result["success"]:
            print("   ✅ Dependencies installed")
        else:
            print(f"   ⚠️  Dependency installation warning: {result.get('stderr', '')[:100]}")
        
        # Summary
        print("\n" + "=" * 60)
        print("📋 Deployment Summary")
        print(f"   Host: {self.host}")
        print(f"   Remote path: {self.remote_path}")
        print(f"   Files deployed: {len(deployed)}")
        if failed:
            print(f"   Failed: {len(failed)} - {', '.join(failed)}")
        
        return {
            "success": len(failed) == 0,
            "deployed": deployed,
            "failed": failed,
            "host": self.host,
            "remote_path": self.remote_path,
        }
    
    def verify_deployment(self) -> Dict[str, Any]:
        """Verify the deployment on remote host."""
        print("\n🔍 Verifying deployment...")
        
        # Check if files exist
        result = self._run_ssh(f"ls -la {self.remote_path}/")
        if not result["success"]:
            return {"success": False, "error": "Failed to list remote directory"}
        
        files = result["stdout"]
        missing = []
        for f in self.FILES_TO_DEPLOY:
            if f not in files:
                missing.append(f)
        
        # Check Python availability
        result = self._run_ssh("python3 --version")
        python_version = result["stdout"].strip() if result["success"] else "Unknown"
        
        # Check if marketing.py is executable
        result = self._run_ssh(f"test -x {self.remote_path}/marketing.py && echo 'executable'")
        is_executable = "executable" in result["stdout"]
        
        print(f"   Python version: {python_version}")
        print(f"   Files present: {len(self.FILES_TO_DEPLOY) - len(missing)}/{len(self.FILES_TO_DEPLOY)}")
        print(f"   Scripts executable: {'Yes' if is_executable else 'No'}")
        
        if missing:
            print(f"   ⚠️  Missing files: {', '.join(missing)}")
        
        return {
            "success": len(missing) == 0 and is_executable,
            "python_version": python_version,
            "missing_files": missing,
            "is_executable": is_executable,
        }
    
    def test_remote_command(self) -> Dict[str, Any]:
        """Test running marketing.py on remote host."""
        print("\n🧪 Testing remote command execution...")
        
        result = self._run_ssh(
            f"cd {self.remote_path} && python3 marketing.py --help",
            timeout=30
        )
        
        if result["success"] and "Marketing Creator" in result["stdout"]:
            print("   ✅ Remote command working")
            return {"success": True}
        else:
            print(f"   ❌ Remote command failed")
            print(f"   Error: {result.get('stderr', 'Unknown error')[:200]}")
            return {"success": False, "error": result.get("stderr")}


def main():
    parser = argparse.ArgumentParser(
        description="Deploy marketing-creator skill to remote host",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Deploy to default host (kai)
  %(prog)s --host myserver    # Deploy to specific host
  %(prog)s --verify           # Verify existing deployment
  %(prog)s --test             # Test remote command execution
        """
    )
    
    parser.add_argument("--host", default="kai",
                       help="SSH host to deploy to (default: kai)")
    parser.add_argument("--verify", action="store_true",
                       help="Verify deployment without deploying")
    parser.add_argument("--test", action="store_true",
                       help="Test remote command after deployment")
    
    args = parser.parse_args()
    
    deployer = Deployer(host=args.host)
    
    if args.verify:
        result = deployer.verify_deployment()
        sys.exit(0 if result["success"] else 1)
    
    # Deploy
    result = deployer.deploy_all()
    
    if not result["success"]:
        print("\n❌ Deployment failed")
        sys.exit(1)
    
    # Verify after deployment
    verify_result = deployer.verify_deployment()
    
    # Test if requested
    if args.test:
        test_result = deployer.test_remote_command()
        if not test_result["success"]:
            print("\n⚠️  Deployment completed but tests failed")
            sys.exit(1)
    
    print("\n✅ Deployment completed successfully!")
    print(f"\nThe marketing-creator skill is now available on {args.host}")
    print(f"Remote path: {deployer.remote_path}")
    print("\nYou can now use the skill on the remote host:")
    print(f"  ssh {args.host}")
    print(f"  cd {deployer.remote_path}")
    print(f"  ./marketing.py image \"Your prompt here\"")


if __name__ == "__main__":
    main()

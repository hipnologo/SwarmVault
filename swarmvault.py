#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import datetime
import argparse
import logging
from pathlib import Path
import tarfile
import shutil
import yaml

class DockerBackupManager:
    def __init__(self, backup_dir="/opt/docker-backups", remote_host=None):
        self.backup_dir = Path(backup_dir)
        self.remote_host = remote_host
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_path = self.backup_dir / self.timestamp
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(f"{self.backup_dir}/backup.log")
            ]
        )
        self.logger = logging.getLogger(__name__)

    def execute_command(self, command, shell=False):
        try:
            if self.remote_host and not shell:
                command = ["ssh", self.remote_host] + command
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                shell=shell,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed: {e.cmd}")
            self.logger.error(f"Error output: {e.stderr}")
            raise

    def backup_portainer_stacks(self):
        """Backup Portainer stacks and their configurations"""
        self.logger.info("Backing up Portainer stacks...")
        stacks_dir = self.backup_path / "portainer/stacks"
        stacks_dir.mkdir(parents=True, exist_ok=True)

        # Get Portainer stack list using Docker API
        stack_list = self.execute_command(
            ["docker", "stack", "ls", "--format", "{{.Name}}"]
        ).split('\n')

        for stack in stack_list:
            if not stack:
                continue
                
            self.logger.info(f"Backing up stack: {stack}")
            
            # Export stack configuration
            try:
                stack_config = self.execute_command(
                    ["docker", "stack", "ps", stack, "--format", "{{json .}}"]
                )
                
                # Save stack configuration
                stack_file = stacks_dir / f"{stack}.json"
                with open(stack_file, 'w') as f:
                    f.write(stack_config)

                # Export compose file if available
                compose_output = self.execute_command(
                    ["docker", "stack", "config", stack],
                    shell=True
                )
                compose_file = stacks_dir / f"{stack}-compose.yml"
                with open(compose_file, 'w') as f:
                    f.write(compose_output)
                    
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Error backing up stack {stack}: {str(e)}")

    def backup_volumes(self):
        """Backup Docker volumes"""
        self.logger.info("Backing up Docker volumes...")
        volumes_dir = self.backup_path / "volumes"
        volumes_dir.mkdir(parents=True, exist_ok=True)

        # Get volume list
        volume_list = self.execute_command(
            ["docker", "volume", "ls", "--format", "{{.Name}}"]
        ).split('\n')

        for volume in volume_list:
            if not volume:
                continue
                
            self.logger.info(f"Backing up volume: {volume}")
            
            try:
                # Create temporary container to backup volume
                backup_container = f"backup-{volume}-{self.timestamp}"
                self.execute_command([
                    "docker", "run", "-d", "--name", backup_container,
                    "-v", f"{volume}:/source:ro",
                    "alpine", "tail", "-f", "/dev/null"
                ])

                # Create tar archive of volume
                volume_backup = volumes_dir / f"{volume}.tar"
                self.execute_command([
                    "docker", "cp",
                    f"{backup_container}:/source/.",
                    str(volumes_dir / volume)
                ])

                # Create tarfile
                with tarfile.open(volume_backup, "w:gz") as tar:
                    tar.add(str(volumes_dir / volume), arcname=volume)

                # Cleanup
                shutil.rmtree(str(volumes_dir / volume))
                self.execute_command(["docker", "rm", "-f", backup_container])
                
            except Exception as e:
                self.logger.error(f"Error backing up volume {volume}: {str(e)}")

    def backup_swarm_config(self):
        """Backup Docker Swarm configuration"""
        self.logger.info("Backing up Swarm configuration...")
        swarm_dir = self.backup_path / "swarm"
        swarm_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Export swarm configuration
            swarm_config = self.execute_command(["docker", "swarm", "inspect"])
            with open(swarm_dir / "swarm-config.json", 'w') as f:
                f.write(swarm_config)

            # Export network configurations
            networks = self.execute_command(
                ["docker", "network", "ls", "--format", "{{.Name}}"]
            ).split('\n')
            
            for network in networks:
                if not network:
                    continue
                    
                network_config = self.execute_command(
                    ["docker", "network", "inspect", network]
                )
                with open(swarm_dir / f"network-{network}.json", 'w') as f:
                    f.write(network_config)

        except Exception as e:
            self.logger.error(f"Error backing up Swarm configuration: {str(e)}")

    def create_backup_archive(self):
        """Create a compressed archive of the entire backup"""
        self.logger.info("Creating backup archive...")
        archive_name = f"docker-backup-{self.timestamp}.tar.gz"
        
        with tarfile.open(self.backup_dir / archive_name, "w:gz") as tar:
            tar.add(self.backup_path, arcname=self.timestamp)

        # Cleanup uncompressed backup directory
        shutil.rmtree(self.backup_path)
        return archive_name

    def sync_to_remote(self, remote_path):
        """Sync backup to remote server"""
        if not self.remote_host:
            self.logger.warning("No remote host specified for sync")
            return

        self.logger.info(f"Syncing backup to {self.remote_host}:{remote_path}")
        try:
            self.execute_command([
                "rsync", "-avz",
                str(self.backup_dir) + "/",
                f"{self.remote_host}:{remote_path}"
            ])
        except Exception as e:
            self.logger.error(f"Error syncing to remote host: {str(e)}")

    def perform_backup(self, sync_to=None):
        """Perform complete backup process"""
        try:
            self.backup_portainer_stacks()
            self.backup_volumes()
            self.backup_swarm_config()
            archive_name = self.create_backup_archive()
            
            if sync_to:
                self.sync_to_remote(sync_to)
                
            self.logger.info(f"Backup completed successfully: {archive_name}")
            return True
        except Exception as e:
            self.logger.error(f"Backup failed: {str(e)}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Docker Environment Backup Tool")
    parser.add_argument("--backup-dir", default="/opt/docker-backups",
                      help="Local backup directory")
    parser.add_argument("--remote-host",
                      help="Remote host for backup operations")
    parser.add_argument("--sync-to",
                      help="Remote path to sync backups to")
    
    args = parser.parse_args()

    backup_manager = DockerBackupManager(
        backup_dir=args.backup_dir,
        remote_host=args.remote_host
    )
    
    success = backup_manager.perform_backup(sync_to=args.sync_to)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
  

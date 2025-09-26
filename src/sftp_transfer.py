import paramiko
import os

class SFTPClient:
    def __init__(self,host,username,password, port=22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.sftp = None
        self.transport = None
        
    def connect(self):
        try:
            # Step 1: Create SSH client object
            ssh_client = paramiko.SSHClient()
            
            # Step 2: Set policy for unknown host keys
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Step 3: Connect to the server
            ssh_client.connect(
                hostname=self.host,
                username=self.username,
                password=self.password,
                port=self.port
            )
            
            # Step 4: Open SFTP session over the SSH connection
            self.sftp = ssh_client.open_sftp()
            self.transport = ssh_client.get_transport()
            
            print(f" Connected to {self.host}")
            
        except Exception as e:
            print(f" Connection failed: {e}")
            raise
    
    def disconnect(self):
        """Close the SFTP connection"""
        if self.sftp:
            self.sftp.close()
        if self.transport:
            self.transport.close()
        print(f" Disconnected from {self.host}")
    
    def list_files(self, remote_directory="/"):
        """List files in a remote directory"""
        try:
            files = self.sftp.listdir(remote_directory)
            print(f" Files in {remote_directory}: {files}")
            return files
        except Exception as e:
            print(f" Error listing files: {e}")
            return []
    
    def download_file(self, remote_file, local_file):
        """Download a file from server to local computer"""
        try:
            self.sftp.get(remote_file, local_file)
            print(f" Downloaded: {remote_file} -> {local_file}")
            return True
        except Exception as e:
            print(f" Download failed: {e}")
            return False
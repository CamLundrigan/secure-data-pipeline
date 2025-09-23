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
            
            print(f"✅ Connected to {self.host}")
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            raise
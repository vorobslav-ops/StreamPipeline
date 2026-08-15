import os
import platform
import shutil
import datetime
import zipfile

class OBSBackupManager:
    def __init__(self):
        # Locate the root of StreamPipeline
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.backup_dir = os.path.join(self.base_dir, "backups", "obs")
        
        # Make sure the backups folder exists locally
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Detect Operating System to find the hidden OBS settings folder
        if platform.system() == "Windows":
            self.obs_config_path = os.path.join(os.environ.get("APPDATA", ""), "obs-studio")
        else:
            self.obs_config_path = os.path.expanduser("~/.config/obs-studio")

    def backup(self):
        if not os.path.exists(self.obs_config_path):
            raise Exception(f"OBS config not found at {self.obs_config_path}. Have you installed OBS yet?")
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"obs_backup_{timestamp}.zip"
        backup_filepath = os.path.join(self.backup_dir, backup_filename)
        
        # Zip the entire OBS directory
        shutil.make_archive(backup_filepath.replace('.zip', ''), 'zip', self.obs_config_path)
        return backup_filename

    def restore(self):
        if not os.path.exists(self.backup_dir):
            raise Exception("No backups directory found.")
            
        backups = [f for f in os.listdir(self.backup_dir) if f.endswith('.zip')]
        if not backups:
            raise Exception("No backup files found in the backups folder.")
            
        # Get the most recent backup
        backups.sort(reverse=True)
        latest_backup = os.path.join(self.backup_dir, backups[0])
        
        # Ensure destination exists
        os.makedirs(self.obs_config_path, exist_ok=True)
        
        # Extract over existing files, restoring widgets, scenes, and settings
        with zipfile.ZipFile(latest_backup, 'r') as zip_ref:
            zip_ref.extractall(self.obs_config_path)
            
        return backups[0]

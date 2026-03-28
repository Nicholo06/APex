import subprocess
import os
from backend.config import config

class ADBDumper:
    def __init__(self, package_name, device_id=None):
        self.package_name = package_name
        self.device_id = device_id
        self.output_dir = os.path.join(config.DOWNLOADS_PATH, package_name)

    def pull_data(self):
        """Pulls sensitive data from the device"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Common target locations
        targets = [
            f"/data/data/{self.package_name}/databases/",
            f"/data/data/{self.package_name}/shared_prefs/",
            f"/data/data/{self.package_name}/lib/"
        ]

        results = []
        adb_base = ["adb"]
        if self.device_id:
            adb_base.extend(["-s", self.device_id])

        for target in targets:
            try:
                # Use adb -s <device> pull to download the directory
                cmd = ["adb"]
                if config.ACTIVE_DEVICE_ID:
                    cmd += ["-s", config.ACTIVE_DEVICE_ID]
                cmd += ["pull", target, self.output_dir]

                subprocess.run(cmd, check=True, capture_output=True)
                results.append({"target": target, "status": "pulled"})

            except subprocess.CalledProcessError as e:
                print(f"Failed to pull {target}: {e}")
                results.append({"target": target, "status": "failed", "error": str(e)})

        return results

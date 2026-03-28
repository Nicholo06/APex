import subprocess
import re

def list_adb_devices():
    """Returns a list of connected ADB devices"""
    try:
        output = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=True).stdout
        lines = output.strip().split('\n')[1:] # Skip header
        devices = []
        for line in lines:
            if line.strip():
                parts = re.split(r'\s+', line)
                if len(parts) >= 2:
                    devices.append({"id": parts[0], "status": parts[1]})
        return devices
    except Exception as e:
        return []

def list_installed_packages(device_id=None):
    """Returns a list of 3rd party installed packages on the device"""
    try:
        cmd = ["adb"]
        if device_id:
            cmd += ["-s", device_id]
        cmd += ["shell", "pm", "list", "packages", "-3"] # -3 filters for 3rd party apps
        
        output = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
        packages = [line.replace("package:", "").strip() for line in output.strip().split('\n') if line.strip()]
        return sorted(packages)
    except Exception as e:
        print(f"[-] Error listing packages: {e}")
        return []

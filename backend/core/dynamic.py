import os
import subprocess
from backend.config import config

class FridaOrchestrator:
    def __init__(self, package_name=None):
        self.package_name = package_name

    def list_scripts(self):
        """Lists available Frida scripts in the user's directory"""
        if not os.path.exists(config.FRIDA_SCRIPTS_PATH):
            os.makedirs(config.FRIDA_SCRIPTS_PATH)
        return [f for f in os.listdir(config.FRIDA_SCRIPTS_PATH) if f.endswith(".js")]

    def attach_and_inject(self, script_name):
        """Uses the native Frida CLI for maximum stability and exact behavior parity"""
        script_path = os.path.join(config.FRIDA_SCRIPTS_PATH, script_name)
        if not os.path.exists(script_path):
            print(f"[-] Error: Script {script_name} not found.")
            return False

        # Build the native frida command
        cmd = ["frida", "-U", "-f", self.package_name, "-l", script_path]
        
        # If a specific device is selected, override the -U flag with -D
        if config.ACTIVE_DEVICE_ID:
            cmd = ["frida", "-D", config.ACTIVE_DEVICE_ID, "-f", self.package_name, "-l", script_path]

        print(f"    [*] Executing Native Command: {' '.join(cmd)}")
        print("    [*] Press Ctrl+C to stop the Frida session and return to APex.\n")

        try:
            # We use call() so the user can interact directly with the Frida CLI if needed, 
            # and to stream all output natively.
            subprocess.call(cmd)
            return True
        except KeyboardInterrupt:
            # User pressed Ctrl+C to exit the Frida session
            print("\n    [*] Frida session closed by user.")
            return True
        except Exception as e:
            print(f"\n    [-] Failed to launch native Frida CLI: {e}")
            print("    [!] Ensure 'frida-tools' is installed and 'frida' is in your system PATH.")
            return False

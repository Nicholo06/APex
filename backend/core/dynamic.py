import frida
import os
from backend.config import config

class FridaOrchestrator:
    def __init__(self, package_name):
        self.package_name = package_name
        self.device = frida.get_usb_device()
        self.session = None

    def list_scripts(self):
        """Lists available Frida scripts in the user's directory"""
        if not os.path.exists(config.FRIDA_SCRIPTS_PATH):
            os.makedirs(config.FRIDA_SCRIPTS_PATH)
        return [f for f in os.listdir(config.FRIDA_SCRIPTS_PATH) if f.endswith(".js")]

    def attach_and_inject(self, script_name):
        """Attaches to the process and injects the selected script"""
        script_path = os.path.join(config.FRIDA_SCRIPTS_PATH, script_name)
        with open(script_path, 'r') as f:
            script_content = f.read()

        try:
            self.session = self.device.attach(self.package_name)
            script = self.session.create_script(script_content)
            script.load()
            return True
        except Exception as e:
            print(f"Injection failed: {e}")
            return False

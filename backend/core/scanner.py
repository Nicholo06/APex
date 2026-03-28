import os
import re
import subprocess
import sys
from backend.config import config

class APKScanner:
    def __init__(self, apk_path):
        self.apk_path = apk_path
        self.output_dir = os.path.join(config.TEMP_DECOMPILED_PATH, os.path.basename(apk_path).replace(".apk", ""))

    def decompile(self):
        """Decompiles the APK using pyapktool via command line"""
        print(f"Decompiling {self.apk_path} to {self.output_dir}...")
        if not os.path.exists(config.TEMP_DECOMPILED_PATH):
            os.makedirs(config.TEMP_DECOMPILED_PATH)
        
        # Call pyapktool's Apktool class directly via python -c
        try:
            cmd = f"{sys.executable} -c \"from pyapktool.pyapktool import Apktool; a=Apktool('pyapktool_tools'); a.get(); a.unpack(r'{self.apk_path}', r'{self.output_dir}')\""
            # Since the library itself might need -f but doesn't expose it easily in unpack(),
            # we check if output_dir exists and clear it if we want to re-decompile.
            import shutil
            if os.path.exists(self.output_dir):
                shutil.rmtree(self.output_dir)
            subprocess.run(cmd, check=True, shell=True)
            return True
        except Exception as e:
            print(f"Decompilation failed: {e}")
            return False

    def find_security_logic(self):
        """Searches for SSL pinning, root detection, API keys, and endpoints"""
        patterns = {
            "ssl_pinning": [
                r"X509TrustManager",
                r"checkClientTrusted",
                r"checkServerTrusted",
                r"SSLContext",
                r"CertificatePinner"
            ],
            "root_detection": [
                r"/system/app/Superuser.apk",
                r"root-checker",
                r"which su",
                r"test-keys"
            ],
            "api_keys": [
                r"AIza[0-9A-Za-z\\-_]{35}", # Google API Key
                r"key-[0-9a-zA-Z]{32}",      # Mailgun API Key
                r"SK[0-9a-fA-F]{32}",        # Twilio API Key
                r"(?:api_key|apiKey|client_secret|firebase_url|google_api_key|google_crash_reporting_api_key)[\"':\s=]+[a-zA-Z0-9_\-]+"
            ],
            "endpoints": [
                r"https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[a-zA-Z0-9./?=_-]*)?"
            ]
        }
        
        # Packages to ignore to reduce noise (standard libraries)
        ignored_packages = [
            "androidx", "android/support", "com/google", "com/facebook",
            "kotlin", "kotlinx", "okhttp3", "okio", "com/swmansion",
            "org/bouncycastle", "expo/modules", "com/caverock", "com/adobe",
            "com/salesforce", "com/pnp", "com/th3rdwave", "org/brotli",
            "com/sslpublickeypinning", "com/horcrux", "com/BV", "com/reactnative",
            "com/dieam", "com/rnfs", "com/learnium", "com/masteratul"
        ]

        # Endpoints to ignore (common library/system URLs)
        ignored_endpoints = [
            "schemas.android.com", "google.com", "github.com", "apache.org",
            "www.w3.org", "android.os.Build", "bouncycastle.org", "xml.org",
            "expo.dev", "filesystem.local", "android.com", "stackoverflow.com",
            "w3.org", "apple.com", "microsoft.com"
        ]

        results = []
        if not os.path.exists(self.output_dir):
            return results

        for root, dirs, files in os.walk(self.output_dir):
            rel_root = os.path.relpath(root, self.output_dir)
            parts = rel_root.split(os.sep)

            # Identify actual package path
            if parts[0].startswith("smali"):
                clean_package_path = "/".join(parts[1:])
            else:
                clean_package_path = rel_root

            for file in files:
                # We now scan Smali for logic, and XML/JSON/Smali for keys/endpoints
                is_smali = file.endswith(".smali")
                is_config = file.endswith(".xml") or file.endswith(".json") or file == "app.config"

                if not (is_smali or is_config):
                    continue

                file_path = os.path.join(root, file)

                # Noise reduction: Skip library Smali files
                if is_smali and any(clean_package_path.startswith(pkg) for pkg in ignored_packages):
                    continue

                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                    # Metadata skip for Smali
                    metadata_start = -1
                    metadata_end = -1
                    if is_smali and ".annotation runtime Lkotlin/Metadata;" in content:
                        metadata_start = content.find(".annotation runtime Lkotlin/Metadata;")
                        metadata_end = content.find(".end annotation", metadata_start)

                    for category, regex_list in patterns.items():
                        # Logic patterns only for Smali
                        if category in ["ssl_pinning", "root_detection"] and not is_smali:
                            continue

                        for regex in regex_list:
                            for match in re.finditer(regex, content, re.IGNORECASE):
                                m_start = match.start()
                                matched_val = match.group()

                                if metadata_start != -1 and metadata_start <= m_start <= metadata_end:
                                    continue

                                if category == "endpoints":
                                    if any(ign in matched_val for ign in ignored_endpoints):
                                        continue
                                    # Basic URL validation to avoid snippets
                                    if len(matched_val) < 10:
                                        continue

                                # Capture context
                                if is_smali:
                                    start = max(0, content.rfind('.method', 0, m_start))
                                    end = content.find('.end method', match.end())
                                    if end != -1: end += 11
                                    else: end = match.end() + 50
                                else:
                                    # For XML/JSON, just take a small window
                                    start = max(0, m_start - 40)
                                    end = min(len(content), match.end() + 40)

                                results.append({
                                    "file": file_path,
                                    "category": category,
                                    "code": content[start:end].strip(),
                                    "match": matched_val
                                })
        return results


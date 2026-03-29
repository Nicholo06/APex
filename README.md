# APex: Advanced APK Explorer and Exfiltrator

**APex** is a professional Android security orchestration suite and a robust wrapper for the Frida framework. It is designed to automate the gap between static analysis and dynamic instrumentation. The tool provides a unified, hyper-contextual CLI environment for rapid security auditing, data exfiltration, and runtime manipulation of Android applications.

---

## Project Goals

The goal of **APex** is to streamline the mobile application penetration testing lifecycle by:
* **Automating Analysis:** High-speed APK decompilation, manifest auditing, and secret sniffing.
* **Simplifying Instrumentation:** Acting as a streamlined wrapper for the Frida framework to manage spawning, attachment, and session lifecycles.
* **Integrated Exfiltration:** Providing a one-click solution for dumping and interactively exploring sensitive app data.
* **Focused Workflow:** A context-aware CLI that dynamically adapts its tools based on the active application in focus.

---

## Key Features

### 1. Intelligent Static Analysis (SAST)
* **Noise-Filtered Scanning:** Automatically filters out Android framework resources to focus exclusively on high-risk application logic and sensitive assets.
* **Manifest Auditing:** Detects critical misconfigurations including debuggable flags, insecure backup settings, and cleartext traffic permissions.
* **Deep Secret Sniffing:** Scans for hardcoded AWS keys, Google API tokens, Firebase URLs, and private certificates across Smali, JSON, and XML files.
* **Report Caching:** Automatically persists scan results to enable near-instant loading of previous security sessions.

### 2. Dynamic Instrumentation (DAST)
* **Frida Wrapper:** Leverages the native Frida CLI for maximum stability while managing the complexities of process spawning and script injection.
* **Multi-Layer Termination:** Implements standard and root-level force-stop sequences to ensure the application and all API connections are fully severed upon exit.
* **Real-time Logging:** Streams standard output and error messages from Frida scripts directly to the consolidated APex console.

### 3. Exfiltrate and Explore Loot
* **Root-Hop Exfiltration:** Uses an automated root-hop method to copy protected data from the application's internal storage to a local environment.
* **Interactive Loot Explorer:** A built-in browser for exfiltrated data, featuring a robust SQLite table viewer and an automated XML/JSON pretty-printer.
* **Binary Safety:** Automatically detects non-text files and provides safe hex dumps for binary inspection.

### 4. Hook Template Generator
* **Reliable Boilerplates:** Provides a library of industry-standard Frida templates for SSL pinning bypass, root detection removal, and Keystore auditing.

---

## Getting Started

### Prerequisites
- Python 3.10+
- Java (JRE/JDK) in your system PATH (required for APKTool operations).
- ADB (Android Debug Bridge) in your system PATH.
- A rooted Android device or emulator with frida-server running in /data/local/tmp/.

### Installation

1. Clone and Enter Folder:
   ```bash
   git clone https://github.com/your-username/APex.git
   cd APex
   ```

2. Setup Environment:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage Guide

APex features a hyper-contextual menu system. To start the tool, run:
```bash
python apex.py
```

### 1. Scan APK
Select Option 1 to begin. You can analyze a new APK file or load a previous session. APex will generate a comprehensive security report covering manifest risks, sensitive assets, and code-level findings.

### 2. Inject Frida Script
Once a session is active, select Option 2 to inject a script. APex automatically targets the active application, lists your local script library, and launches the app using the native Frida wrapper.

### 3. Exfiltrate and Explore Loot
Select Option 3 to pull the app's internal databases and shared preferences. Once exfiltrated, APex immediately opens the Loot Explorer, allowing you to browse SQLite tables and view configuration files directly in the terminal.

### 4. Hook Template Generator
Select Option 4 to generate functional Frida bypass scripts. Templates are saved to the local script folder and are ready for immediate injection.

### 5. Switch App / New Scan
Select Option 5 to clear the current context and return to the main menu to target a different application.

---

## Disclaimer
**APex** is intended for authorized security auditing and educational purposes only. Unauthorized access to computer systems is illegal. The author is not responsible for any misuse of this tool.

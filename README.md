APex: AI-Powered APK Explorer & Exfiltrator
APex is an advanced Android security orchestration suite designed to bridge the gap between static analysis and dynamic instrumentation. By integrating LLMs (Large Language Models) directly into the reverse-engineering workflow, APex automates the discovery and bypassing of complex security controls like SSL pinning and root detection.

🎯 Project Goals & Purpose
The goal of APex is to reduce the manual effort required during the initial phases of a mobile application penetration test. It aims to:

Automate the "Boring" Stuff: Fast-track APK decompilation, secret sniffing, and permission auditing.

Bridge RE Gaps with AI: Use AI to interpret obfuscated Smali logic and generate functional Frida hooks.

Centralize Exfiltration: Provide a one-click solution for dumping sensitive app data (databases, native libs, and configurations).

Flexible Orchestration: Offer a "Bring Your Own Script" (BYOS) environment for seasoned pentesters.

✨ Key Features
🔍 1. Intelligent Static Analysis (SAST)
Automated Decompilation: Leverages apktool to crack open APKs instantly.

Secret Sniffer: Regex-based scanning for API keys, Firebase URLs, hardcoded credentials, and RSA keys.

Manifest Auditor: Identifies dangerous permissions and exported components that lead to Intent Redirection or Provider leakage.

💉 2. Dynamic Instrumentation (DAST)
Frida Orchestrator: Attach to running processes and inject JS hooks on the fly.

BYOS Logic: Includes a dedicated /frida-scripts directory. Just drop your universal.js or multiple.js into the folder, and APex will auto-detect and load them via the dashboard.

🤖 3. AI-Assisted Bypass Engine
Surgical Hooking: When standard scripts fail, APex extracts the relevant Smali code for the security check.

LLM Integration: Connects to Gemini (or Claude) to analyze the logic and generate a custom JavaScript hook tailored specifically to that app’s implementation.

💾 4. Data Exfiltration Suite
Database Dumper: Automatically pulls SQLite .db files from /data/data/[pkg]/.

Native Library Extraction: Pulls .so files for offline binary analysis (Ghidra/IDA).

Config Grabber: Extracts shared_prefs and other XML configurations.

🛠️ Tech Stack
Backend: Python 3.10+, FastAPI

Analysis: Scapy, Frida-Tools, Apktool

AI: Google Generative AI (Gemini API)

Frontend: JavaScript (ES6+), Tailwind CSS

Database: SQLite (for local device tracking)

🚀 Getting Started
Prerequisites
Python 3.10+

ADB (Android Debug Bridge) in your system PATH.

A rooted Android device or emulator with frida-server running.

(Optional) An API Key for Gemini or Claude for AI features.

Installation
Clone the Repository:

Bash
git clone https://github.com/your-username/apex-toolkit.git
cd apex-toolkit
Add Your Scripts:
Place your existing Frida scripts in the frida-scripts/ directory.

Setup Environment:

Bash
pip install -r requirements.txt
cp .env.example .env # Add your API keys here
Run APex:

Bash
python backend/main.py
📖 Usage
Upload: Drag an APK into the APex Dashboard.

Analyze: Run the Static Scan to find hardcoded secrets.

Inject: Select a script from your /frida-scripts library and click Inject.

AI Bypass: If traffic is still blocked, select the "Generate AI Hook" option to have APex analyze the Smali and create a custom bypass.

Exfiltrate: Use the "Dump Data" button to pull all internal files to your local /downloads folder.

⚖️ Disclaimer
APex is intended for authorized security auditing and educational purposes only. Unauthorized access to computer systems is illegal. The author is not responsible for any misuse of this tool.
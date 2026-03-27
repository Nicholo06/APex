import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    AI_PROVIDER = os.getenv("AI_PROVIDER", "google")
    FRIDA_SCRIPTS_PATH = os.getenv("FRIDA_SCRIPTS_PATH", "./frida-scripts")
    TEMP_DECOMPILED_PATH = "./temp_decompiled"
    DOWNLOADS_PATH = "./downloads"

config = Config()

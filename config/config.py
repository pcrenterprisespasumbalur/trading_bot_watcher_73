import json
import os
from cryptography.fernet import Fernet

# Load encryption key
KEY_FILE = "config/secret.key"
ENC_FILE = "config/config.enc"

with open(KEY_FILE, "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)

# Read encrypted API keys
with open(ENC_FILE, "rb") as enc_file:
    encrypted_keys = enc_file.readlines()

API_KEY = cipher.decrypt(encrypted_keys[0]).decode()
API_SECRET = cipher.decrypt(encrypted_keys[1]).decode()

# Load settings from JSON
SETTINGS_FILE = "config/settings.json"

with open(SETTINGS_FILE, "r") as f:
    settings = json.load(f)

COIN_NAME = settings["COIN_NAME"]
TRADE_AMOUNT = settings["TRADE_AMOUNT"]
TIMEFRAME = settings["TIMEFRAME"]
LIMIT = settings["LIMIT"]

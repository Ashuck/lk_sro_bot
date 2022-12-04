import json, yaml
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "config.yaml") as f:
    config = yaml.safe_load(f)

TOKEN = os.environ.get("BOT_TOKEN")
SOURCES = config["sources"]
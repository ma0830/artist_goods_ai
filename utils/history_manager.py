'''
Created on 2025/09/04

@author: 81901
'''
# utils/history_manager.py
import json
from datetime import datetime
import os

HISTORY_FILE = "goods_history.json"

def save_history(artist_name: str, theme: str, style: str, ideas: str):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "artist_name": artist_name,
        "theme": theme,
        "style": style,
        "ideas": ideas
    }

    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []

    history.append(entry)

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

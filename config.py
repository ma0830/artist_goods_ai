'''
Created on 2025/09/04

@author: 81901
'''
# config.py
import os
from dotenv import load_dotenv

# .env を読み込む
load_dotenv()

# OpenAI & Replicate APIキーを取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

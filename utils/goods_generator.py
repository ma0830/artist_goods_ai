'''
Created on 2025/09/04

@author: 81901
'''
# utils/goods_generator.py
import openai
import os
from dotenv import load_dotenv

# .envからAPIキー読み込み
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAIクライアント初期化（新仕様）
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_goods_ideas(artist_name, theme, style):
    prompt = f"""
    アーティスト「{artist_name}」のために、テーマ「{theme}」、スタイル「{style}」に合ったグッズ案を5つ考えてください。
    それぞれの案に簡単な説明もつけてください。
    """

    messages = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )

    ideas = response.choices[0].message.content.strip()
    return ideas

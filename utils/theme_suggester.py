'''
Created on 2025/09/04

@author: 81901
'''
# utils/theme_suggester.py
import openai
from config import OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def suggest_themes(artist_name: str) -> list:
    prompt = f"{artist_name}に合いそうなグッズのテーマを5つ、短く提案してください。"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=150
    )

    raw = response.choices[0].message.content.strip()
    return [line.strip("-・ ") for line in raw.split("\n") if line]


'''
Created on 2025/09/04

@author: 81901
'''
# utils/image_generator.py
import openai
from config import OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_image(prompt: str) -> str:
    response = client.images.generate(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    return response.data[0].url


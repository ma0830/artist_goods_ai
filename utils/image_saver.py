'''
Created on 2025/09/04

@author: 81901
'''
# utils/image_saver.py
import requests
from PIL import Image
from io import BytesIO

def download_image(url: str) -> Image.Image:
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

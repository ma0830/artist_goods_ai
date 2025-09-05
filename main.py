# main.py
'''
Created on 2025/09/04
@author: 81901
'''

import streamlit as st
import os
from dotenv import load_dotenv
import replicate
import openai
import requests
from PIL import Image
import io
import re

# 自作モジュール
from config import OPENAI_API_KEY
from utils.goods_generator import generate_goods_ideas
from utils.history_manager import save_history, load_history
from utils.logger import log_event, log_error

# .env 読み込み
load_dotenv()
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
client = openai.OpenAI(api_key=OPENAI_API_KEY)

st.set_page_config(page_title="Artist Goods AI", layout="centered")
st.title("🎨 Artist Goods AI")
st.write("アーティスト向けグッズ案をAIで生成するアプリです！")

# グッズ案生成
if not OPENAI_API_KEY or OPENAI_API_KEY.startswith("sk-..."):
    st.error("OpenAI APIキーが未設定です。config.pyまたは.envを確認してください。")
else:
    artist_name = st.text_input("アーティスト名を入力")
    theme = st.text_input("テーマ（例: 星空、自然、夢など）")
    style = st.selectbox("スタイル", ["かわいい", "かっこいい", "シンプル", "幻想的", "ポップ"])

    if st.button("グッズ案を生成！"):
        if artist_name and theme:
            with st.spinner("AIが考え中...💭"):
                try:
                    messages = [
                        {"role": "system", "content": "あなたはグッズ企画のプロです。"},
                        {"role": "user", "content": f"{artist_name}向けに、{theme}をテーマにした{style}スタイルのグッズ案を考えてください。"}
                    ]
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=messages
                    )
                    ideas = response.choices[0].message.content

                    st.success("グッズ案が生成されました！")
                    st.text_area("提案されたグッズ案", ideas, height=200)

                    save_history(artist_name, theme, style, ideas)
                    log_event(f"Generated ideas for {artist_name} with theme '{theme}' and style '{style}'")
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")
                    log_error(str(e))
        else:
            st.warning("アーティスト名とテーマを入力してください。")

    if st.checkbox("過去の履歴を見る"):
        history = load_history()
        if history:
            for entry in reversed(history[-5:]):
                st.markdown(f"**{entry['timestamp']}**")

# 画像生成セクション
st.header("🎨 グッズ画像を生成しよう！")

product_type = st.text_input("グッズ種別", placeholder="例：アクリルキーホルダー、スマホケース、ぬいぐるみなど")
theme = st.text_input("雰囲気やテーマ", placeholder="例：かわいい、レトロ、ダーク、和風、未来感など")
style = st.selectbox("生成画像のスタイル", ["実写風", "イラスト風", "ラフ画風", "3Dグラフィック風", "その他"])
material = st.selectbox("素材", ["アクリル", "プラスチック", "布製", "金属", "木製", "ガラス", "陶器", "紙", "液状", "ビニール", "その他"])
extra_input = st.text_area("そのほか自由な要望や商品説明はコチラに書いてね", placeholder="例：赤色、ラメ付き、～みたいなグッズにして")

# 色抽出（簡易）
color_keywords = ["赤", "青", "緑", "黄色", "紫", "黒", "白", "ピンク", "オレンジ", "水色", "茶色", "グレー"]
found_colors = [c for c in color_keywords if c in extra_input]
color_prompt = "、".join(found_colors) + "の色を使用した" if found_colors else ""

# 自動補完文
extra = f"{extra_input}。これは販売用グッズの商品画像です。人物や風景ではありません。単体で写っていて白背景。商品写真風。{color_prompt}"

# 素材補完
material_details = {
    "アクリル": "透明なアクリル素材、平面、印刷された",
    "プラスチック": "光沢のあるプラスチック素材、軽量",
    "布製": "柔らかい布素材、縫い目が見える、衣類、アパレル、小物",
    "金属": "金属の質感、重厚感、冷たい光沢",
    "木製": "木目のある表面、ナチュラルな質感",
    "ガラス": "透明で反射するガラス素材、繊細な光の表現",
    "陶器": "滑らかな陶器の質感、丸みのある形状",
    "紙": "紙の質感、印刷された表面、軽量",
    "液状": "液体のような質感、透明感、流動的な形",
    "ビニール": "ビニール素材のポーチやケース、柔らかく光沢のある表面",
    "その他": ""
}
positive_detail = material_details.get(material, "")
positive_detail += " グッズ、商品画像、商品写真風、ECサイト風、アーティストグッズ、ファングッズ"

# Negative Prompt（最大強化＋意味不明な物体除外）
negative_prompt = (
    "bedroom, bed, pillow, blanket, interior, furniture, "
    "medical, medicine, pill, syringe, bottle, container, hospital, healthcare, diagnostic, sterile, "
    "landscape, scenery, city, town, sky, ocean, underwater, street, building, "
    "food, meal, dish, cuisine, cooking, kitchen, fruit, apple, banana, orange, strawberry, grapes, melon, "
    "animal, pet, creature, human, person, face, portrait, woman, girl, female, lady, young woman, anime girl, idol, character portrait, "
    "abstract object, unknown item, random shape, blob, unidentifiable"
)

# プロンプト構築
prompt = f"{product_type}、{style}、{theme}な雰囲気の商品画像。{extra}。{positive_detail}"

if st.button("画像を生成！"):
    with st.spinner("画像を生成中..."):
        try:
            image_url = replicate.run(
                "lucataco/realistic-vision-v5.1:2c8e954decbf70b7607a4414e5785ef9e4de4b8c51d50fb8b8b349160e0ef6bb",
                input={
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "width": 512,
                    "height": 512,
                    "num_inference_steps": 25,
                    "guidance_scale": 5
                }
            )

            response = requests.get(image_url)
            image = Image.open(io.BytesIO(response.content))

            st.image(image, caption="生成されたグッズ画像", use_container_width=True)
            log_event(f"Generated image with prompt: {prompt}")
        except Exception as e:
            st.error(f"画像生成中にエラーが発生しました: {e}")
            log_error(str(e))




import streamlit as st
from openai import OpenAI
import io
import base64
from PIL import Image
from dotenv import load_dotenv, set_key
import os

# ===== 環境変数ロード =====
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ===== OpenAIクライアント初期化 =====
client = OpenAI(api_key=api_key)

# ===== OCR処理関数 =====
def perform_ocr(image):
    """
    OpenAI GPT-4 Visionを使用してOCRを実行する
    """
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')  # PNG形式で保存
    image_bytes.seek(0)
    
    # Base64エンコード
    base64_image = base64.b64encode(image_bytes.getvalue()).decode("utf-8")
    img_url = f"data:image/png;base64,{base64_image}"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": 
                        """
                            添付画像を読み取り、必ずHTML形式で再現してください。
                            ただし、形式的なものなので、bodyタグの中身だけで構いません。
                            読み取れない場合もpタグでその旨を記載してください。
                        """
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": img_url},
                    },
                ],
            }
        ],
    )
    return response.choices[0].message.content

# ===== Streamlit UI =====
uploaded_file = st.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
    
    # OpenAI APIで画像をHTMLに変換
    extracted_html = perform_ocr(image)

    st.subheader("Result")
    st.markdown(extracted_html, unsafe_allow_html=True)  # HTMLをレンダリング

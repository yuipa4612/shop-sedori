import streamlit as st
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="店舗リサーチ・価格検索くん", layout="centered")

def setup_ai():
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("設定：Secretsにキーが見つかりません。")
        return False
    key = st.secrets["GEMINI_API_KEY"].strip().strip('"').strip("'")
    genai.configure(api_key=key)
    return True

st.title("🚀 店舗リサーチ・価格検索くん")
st.caption("【西野さん専用】利益2,000円判定・エラー回避版")

if setup_ai():
    st.subheader("📸 商品を撮影する")
    uploaded_file = st.file_uploader("ここをタップして、商品の写真を撮ってください", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="分析しています...", use_container_width=True)
        
        with st.spinner("AIが調査中..."):
            success = False
            # 承認待ちを回避するため3つのモデルを試す
            models_to_try = ['gemini-1.5-flash-8b', 'gemini-1.5-flash', 'gemini-1.0-pro-vision-latest']
            
            for model_name in models_to_try:
                try:
                    model = genai.GenerativeModel(model_name)
                    prompt = "この商品について、メルカリ検索用のキーワードを抽出してください。"
                    response = model.generate_content([prompt, image])
                    words = response.text.strip().replace("\n", " ")
                    
                    if words:
                        st.success(f"特定しました： {words}")
                        url = f"https://jp.mercari.com/search?keyword={words}&status=sold_out%7Ctrading&order=desc"
                        st.link_button("👉 メルカリで確認する", url)
                        success = True
                        break 
                except Exception:
                    continue 
            
            if not success:
                st.error("【最終エラー】Google側の承認が降りていません。")

# 利益計算
st.divider()
st.subheader("💰 2,000円利益計算")
col1, col2 = st.columns(2)
with col1:
    sell = st.number_input("売価 (円)", min_value=0, step=100)
with col2:
    buy = st.number_input("仕入 (円)", min_value=0, step=100)
if sell > 0:
    profit = int(sell * 0.9) - buy - 1000
    st.metric("利益", f"{profit:,} 円")
    if profit >= 2000: st.success("✅ 利益2,000円クリア！")

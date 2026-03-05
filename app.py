import streamlit as st
from PIL import Image
import google.generativeai as genai

# 設定
st.set_page_config(page_title="Shop Sedori Pro", layout="centered")

def setup_ai():
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Secretsにキーがありません。")
        return False
    # 前後のゴミを徹底排除
    key = st.secrets["GEMINI_API_KEY"].strip().strip('"').strip("'")
    genai.configure(api_key=key)
    return True

st.title("🚀 店舗リサーチ・価格検索くん")
st.caption("【西野さん専用】404回避・多重モデル試行版")

if setup_ai():
    file = st.file_uploader("写真を撮る", type=["jpg", "jpeg", "png"])
    if file:
        img = Image.open(file)
        st.image(img, use_column_width=True)
        with st.spinner("分析中..."):
            # 使えるモデルを順に試す（404対策の究極系）
            models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-1.0-pro-vision-latest']
            success = False
            for m in models_to_try:
                try:
                    model = genai.GenerativeModel(m)
                    res = model.generate_content(["この商品のメーカー名、型番を抽出してください。", img])
                    words = res.text.strip().replace("\n", " ")
                    st.success(f"検索ワード: {words}")
                    st.markdown(f"### 🔍 [メルカリ相場を確認する](https://jp.mercari.com/search?keyword={words}&status=sold_out%7Ctrading&order=desc)")
                    success = True
                    break
                except:
                    continue
            
            if not success:
                st.error("【404】すべてのモデルへのアクセスがGoogleに拒絶されました。APIキーを新しく作り直してください。")

# 利益計算
st.divider()
st.subheader("💰 2,000円利益計算")
sell = st.number_input("予想売価 (円)", min_value=0, step=100)
buy = st.number_input("仕入れ値 (円)", min_value=0, step=100)
if sell > 0:
    profit = int(sell * 0.9) - buy - 1000
    st.metric("利益", f"{profit:,} 円")
    if profit >= 2000: st.success("✅ 利益2,000円クリア！")

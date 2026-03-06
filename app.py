import streamlit as st
from PIL import Image
import google.generativeai as genai

# 西野さん専用：アプリ名と日本語化を完全反映
st.set_page_config(page_title="店舗リサーチ・価格検索くん", layout="centered")

def setup_ai():
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("設定：Secretsにキーが見つかりません。")
        return False
    # 鍵の不純物を徹底排除
    key = st.secrets["GEMINI_API_KEY"].strip().strip('"').strip("'")
    genai.configure(api_key=key)
    return True

st.title("🚀 店舗リサーチ・価格検索くん")
st.caption("【西野さん専用】利益2,000円判定・日本語安定版")

if setup_ai():
    st.subheader("📸 商品を撮影する")
    uploaded_file = st.file_uploader("ここをタップして、商品の写真を撮ってください", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="分析しています...", use_container_width=True)
        
        with st.spinner("AIが調査中..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = "この商品について、メルカリ検索用のキーワード（メーカー名、商品名、型番）を抽出してください。説明は不要です。"
                response = model.generate_content([prompt, image])
                words = response.text.strip().replace("\n", " ")
                
                if words:
                    st.success(f"特定しました： {words}")
                    url = f"https://jp.mercari.com/search?keyword={words}&status=sold_out%7Ctrading&order=desc"
                    st.link_button("👉 メルカリで「売り切れ価格」を確認する", url)
            except Exception as e:
                st.error("【分析失敗】Google側の承認待ちの可能性があります。")
                st.code(str(e))

# 利益計算機
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

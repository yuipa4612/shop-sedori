import streamlit as st
from PIL import Image
import google.generativeai as genai

# アプリのタイトル
st.set_page_config(page_title="店舗リサーチ・価格検索くん", layout="centered")

# API設定（不純物を徹底排除）
def setup():
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("設定：Secretsにキーが見つかりません。")
        return False
    # 完全に空白や引用符を削る
    key = st.secrets["GEMINI_API_KEY"].strip().strip('"').strip("'")
    genai.configure(api_key=key)
    return True

st.title("🚀 店舗リサーチ・価格検索くん")
st.caption("【西野さん専用】シンプル動作検証版")

if setup():
    # 日本語の案内を強調
    st.subheader("📸 商品を撮影する")
    uploaded_file = st.file_uploader(
        "ここをタップして写真を撮ってください", 
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="分析しています...", use_container_width=True)
        
        with st.spinner("AIが調査中..."):
            try:
                # 【404対策】現在Googleで最も『無難』とされる旧来の呼び出し方を採用
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                
                # 最も短い命令
                prompt = "この商品について、メルカリ検索用のキーワード（メーカー、商品名、型番）を短く教えてください。"
                response = model.generate_content([prompt, image])
                
                words = response.text.strip().replace("\n", " ")
                if words:
                    st.success(f"特定しました： {words}")
                    # メルカリ検索リンク
                    url = f"https://jp.mercari.com/search?keyword={words}&status=sold_out%7Ctrading&order=desc"
                    st.link_button("👉 メルカリで「売り切れ価格」を確認する", url)
                
            except Exception as e:
                # 404が出た場合のみ、特別なメッセージを出す
                error_msg = str(e)
                if "404" in error_msg:
                    st.error("【404エラー：未承認】")
                    st.write("Google側で、西野さんのAPIキーに画像分析の許可がまだ下りていないようです。")
                    st.info("このエラーは、新しいキーを発行してから数時間〜1日経つと自然に解決することがあります。")
                else:
                    st.error(f"分析失敗: {error_msg}")

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
    st.metric("見込み利益", f"{profit:,} 円")
    if profit >= 2000: st.success("✅ 利益2,000円クリア！")

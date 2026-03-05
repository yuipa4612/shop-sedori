import streamlit as st
from PIL import Image
import google.generativeai as genai
import os

# 1. ページ初期設定
st.set_page_config(page_title="Shop Sedori Pro", layout="centered")

# 2. APIキーの強制クリーンアップと再読み込み
def configure_gemini():
    try:
        # Secretsから取得し、前後の空白や改行を完全に排除
        raw_key = st.secrets["GEMINI_API_KEY"]
        clean_key = raw_key.strip().strip('"').strip("'")
        genai.configure(api_key=clean_key)
        return True
    except Exception as e:
        st.error(f"【設定エラー】Secretsの確認が必要です: {e}")
        return False

# 3. メイン画面
st.title("🚀 店舗リサーチ・価格検索くん")
st.caption("西野さん専用：最高精度のAIモデルでリサーチします")

# 設定実行
if configure_gemini():
    uploaded_file = st.file_uploader("商品の写真を撮る", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="分析中...", use_column_width=True)
        
        with st.spinner("AIがメルカリ相場を特定中..."):
            try:
                # 404/429エラーを最も回避しやすい安定モデルを指定
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # 画像分析の実行
                prompt = "この商品についてメルカリで検索するための『メーカー名 商品名 型番』を抽出してください。余計な説明は一切不要です。"
                response = model.generate_content([prompt, image])
                
                # 結果の表示
                search_keywords = response.text.strip().replace("\n", " ")
                if search_keywords:
                    st.success(f"検索ワード: {search_keywords}")
                    mercari_url = f"https://jp.mercari.com/search?keyword={search_keywords}&status=sold_out%7Ctrading&order=desc"
                    st.markdown(f"### 🔍 [ここを押してメルカリ相場を確認する]({mercari_url})")
                
            except Exception as e:
                # エラーが出た場合、原因を特定するための詳細情報を表示
                st.error("【分析エラー】以下のメッセージを教えてください。")
                st.code(str(e))

# 4. 利益計算機（常に表示）
st.divider()
st.subheader("💰 2,000円利益計算")
col1, col2 = st.columns(2)
with col1:
    sell = st.number_input("予想売値 (円)", min_value=0, step=100)
with col2:
    buy = st.number_input("仕入れ値 (円)", min_value=0, step=100)

if sell > 0:
    # 手数料10%、送料目安1000円で計算
    profit = int(sell * 0.9) - buy - 1000
    st.metric("見込み利益", f"{profit:,} 円")
    if profit >= 2000:
        st.success("✅ 利益2,000円クリア！")

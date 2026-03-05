import streamlit as st
from PIL import Image
import google.generativeai as genai

# 1. ページ初期設定
st.set_page_config(page_title="Shop Sedori Pro", layout="centered")

# 2. API設定の実行（エラーを徹底排除）
def setup_ai():
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("【設定ミス】Secretsに『GEMINI_API_KEY』が登録されていません。")
        return None
    
    # 鍵から余計な文字（スペースや引用符）を完全に削る
    api_key = st.secrets["GEMINI_API_KEY"].strip().strip('"').strip("'")
    genai.configure(api_key=api_key)
    return True

# 3. メイン画面
st.title("🚀 店舗リサーチ・価格検索くん")
st.caption("西野さん専用：エラー自動回避機能付き")

if setup_ai():
    uploaded_file = st.file_uploader("商品の写真を撮る", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="分析中...", use_column_width=True)
        
        with st.spinner("AIがメルカリ相場を特定中..."):
            # 【404対策】使えるモデルを順番にすべて試す「全当たり作戦」
            target_models = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-1.5-flash-8b']
            success = False
            
            for model_name in target_models:
                try:
                    model = genai.GenerativeModel(model_name)
                    prompt = "この商品についてメルカリで検索するための『メーカー名 商品名 型番』を抽出してください。余計な説明は不要です。"
                    response = model.generate_content([prompt, image])
                    
                    search_keywords = response.text.strip().replace("\n", " ")
                    if search_keywords:
                        st.success(f"検索ワード: {search_keywords}")
                        mercari_url = f"https://jp.mercari.com/search?keyword={search_keywords}&status=sold_out%7Ctrading&order=desc"
                        st.markdown(f"### 🔍 [メルカリ相場を確認する]({mercari_url})")
                        success = True
                        break # 成功したら終了
                except Exception:
                    continue # 404が出たら次のモデルを試す
            
            if not success:
                st.error("【重大なエラー】すべてのAIモデルが拒絶されました。")
                st.info("APIキー自体が無効、または期限切れの可能性があります。再度キーの発行を確認してください。")

# 4. 利益計算機
st.divider()
st.subheader("💰 2,000円利益計算")
col1, col2 = st.columns(2)
with col1:
    sell = st.number_input("予想売価 (円)", min_value=0, step=100)
with col2:
    buy = st.number_input("仕入れ値 (円)", min_value=0, step=100)

if sell > 0:
    profit = int(sell * 0.9) - buy - 1000
    st.metric("見込み利益", f"{profit:,} 円")
    if profit >= 2000:
        st.success("✅ 利益2,000円クリア！")

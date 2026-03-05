import streamlit as st
from PIL import Image
import google.generativeai as genai

# 1. ページの設定
st.set_page_config(page_title="Shop Sedori Pro", layout="centered")

# 2. AIの設定（エラーを徹底的に回避する最新の書き方）
def setup_ai():
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("【設定エラー】SecretsにAPIキーが登録されていません。")
        return False
    
    # 引用符や空白が混じっていても自動で削除する
    api_key = st.secrets["GEMINI_API_KEY"].strip().strip('"').strip("'")
    genai.configure(api_key=api_key)
    return True

# --- メイン画面 ---
st.title("🚀 店舗リサーチ・価格検索くん")
st.caption("【西野さん専用】エラー自動回避機能付き・最新版")

if setup_ai():
    # 写真アップロード
    uploaded_file = st.file_uploader("商品の写真を撮る（または選ぶ）", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="AIが分析しています...", use_column_width=True)
        
        with st.spinner("メルカリの売れ行きを調査中..."):
            try:
                # 404エラーを回避するため、最も汎用的なモデル名を指定
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # 商品特定のための指示
                prompt = "この画像から『メーカー名 商品名 型番』を抜き出してください。検索用なので余計な説明は不要です。"
                response = model.generate_content([prompt, image])
                
                # 検索用キーワードの整理
                search_keywords = response.text.strip().replace("\n", " ")
                
                if search_keywords:
                    st.success(f"検索ワードを特定しました: {search_keywords}")
                    # メルカリの「売り切れ（SOLD）」に絞った検索URL
                    mercari_url = f"https://jp.mercari.com/search?keyword={search_keywords}&status=sold_out%7Ctrading&order=desc"
                    st.markdown(f"### 🔍 [メルカリで相場を確認する]({mercari_url})")
            
            except Exception as e:
                st.error("【分析エラー】AIの扉が開きませんでした。")
                st.write(f"原因: {e}")
                st.info("※もし404が出る場合は、Secretsに入れたAPIキーが最新のものか再確認してください。")

# 利益計算機
st.divider()
st.subheader("💰 2,000円利益計算")
col1, col2 = st.columns(2)
with col1:
    sell = st.number_input("メルカリ予想売価 (円)", min_value=0, step=100)
with col2:
    buy = st.number_input("店舗の仕入れ価格 (円)", min_value=0, step=100)

if sell > 0:
    fee = int(sell * 0.1) # 手数料10%
    shipping = 1000       # 送料目安
    profit = sell - buy - fee - shipping
    st.metric("見込み純利益", f"{profit:,} 円")
    
    if profit >= 2000:
        st.success("✅ 利益2,000円クリア！仕入れ対象です！")
    else:
        st.warning(f"⚠️ あと {2000-profit:,}円 利益が足りません")

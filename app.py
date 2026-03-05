import streamlit as st
from PIL import Image
import google.generativeai as genai

# --- ページ基本設定 ---
st.set_page_config(page_title="Shop Sedori Pro", layout="centered")

# APIキーの読み込みと設定
try:
    # Secretsからキーを取得
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("APIキーが設定されていません。Streamlit CloudのSecretsを確認してください。")

# --- アプリの見た目 ---
st.title("🚀 店舗リサーチ・価格検索くん")
st.caption("【西野さん専用】写真を撮るだけでメルカリ相場を瞬時に分析")

# --- 画像リサーチ機能 ---
st.subheader("📸 商品を撮影して分析")
uploaded_file = st.file_uploader("商品の全体写真または型番をアップロード", type=["jpg", "jpeg", "png"])

search_keywords = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="分析中の商品", use_column_width=True)
    
    with st.spinner("AIが最速で商品を特定中..."):
        try:
            # 【404対策】Google AI Studioで現在最も安定して動く最新モデルを指定
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # 画像から検索キーワードを抽出
            prompt = "この画像の商品をメルカリで検索したいです。メーカー名、商品名、型番を抜き出してスペース区切りで教えてください。説明文は一切不要です。"
            
            response = model.generate_content([prompt, image])
            search_keywords = response.text.strip().replace("\n", " ")
            
            if search_keywords:
                st.success(f"検索ワードを生成しました: {search_keywords}")
        except Exception as e:
            # エラーの詳細を表示しつつ、対策を表示
            st.error(f"分析エラーが発生しました。")
            st.write(f"エラー詳細: {e}")
            st.info("※もし404が消えない場合、APIキー自体がこのモデルを許可していない可能性があります。")

# --- メルカリ検索リンク ---
if search_keywords:
    # 売り切れ（SOLD）に絞った検索URL
    mercari_url = f"https://jp.mercari.com/search?keyword={search_keywords}&status=sold_out%7Ctrading&order=desc"
    st.markdown(f"### 🔍 [メルカリで相場を確認する]({mercari_url})")

# --- 利益計算機 ---
st.divider()
st.subheader("💰 2,000円利益シミュレーション")

col1, col2 = st.columns(2)
with col1:
    sell_price = st.number_input("予想売価 (円)", min_value=0, step=100)
with col2:
    buy_price = st.number_input("仕入れ価格 (円)", min_value=0, step=100)

if sell_price > 0:
    fee = int(sell_price * 0.1)
    shipping = 1000  # 標準的な送料
    profit = sell_price - buy_price - fee - shipping
    
    st.metric("見込み純利益", f"{profit:,} 円")
    
    if profit >= 2000:
        st.success("✅ 利益2,000円達成！これは『買い』です！")
    else:
        st.warning(f"⚠️ あと {2000-profit:,}円 利益が足りません")

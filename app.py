import streamlit as st
from PIL import Image
import google.generativeai as genai

# --- 設定 ---
st.set_page_config(page_title="Shop Sedori Pro", layout="centered")

# Streamlit SecretsからAPIキーを取得
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("APIキーが設定されていません。StreamlitのSecretsに 'GEMINI_API_KEY' を登録してください。")

# --- タイトル ---
st.title("🚀 店舗リサーチ・価格検索くん")
st.caption("写真を撮るだけで、メルカリの『販売価格付き』一覧を表示します！")

# --- 画像解析セクション ---
st.subheader("📸 写真で相場（価格）を調べる")
uploaded_file = st.file_uploader("商品の全体写真を撮る、または選ぶ", type=["jpg", "jpeg", "png"])

search_keywords = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="この商品をリサーチ中...", use_column_width=True)
    
    with st.spinner("AIが商品の特徴と価格相場を分析中..."):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = "この画像の商品をメルカリで探すための、最も適切な『メーカー名』『商品名』『特徴（色や形）』を教えてください。余計な説明は不要です。例：パナソニック 炊飯器 白 5.5合"
            response = model.generate_content([prompt, image])
            search_keywords = response.text.strip().replace("\n", " ")
            st.success(f"検索ワード: {search_keywords}")
        except Exception as e:
            st.error(f"分析エラー: {e}")

# --- 検索実行セクション ---
if search_keywords:
    mercari_url = f"https://jp.mercari.com/search?keyword={search_keywords}&status=sold_out%7Ctrading&order=desc"
    st.markdown(f"### 🔍 [ここを押して『販売価格』を確認する]({mercari_url})")

# --- 利益計算セクション ---
st.divider()
st.subheader("💰 2,000円利益シミュレーション")

sell_price = st.number_input("メルカリでの販売済価格 (円)", min_value=0, step=100)
buy_price = st.number_input("目の前の店舗価格 (円)", min_value=0, step=100)

if sell_price > 0:
    fee = int(sell_price * 0.1)
    shipping = 1000
    profit = sell_price - buy_price - fee - shipping
    st.metric("見込み純利益", f"{profit:,} 円")
    
    if profit >= 2000:
        st.success("✅ 利益2,000円クリア！これは『買い』です！")
    else:
        st.error(f"❌ あと {2000-profit:,}円 利益が足りません")

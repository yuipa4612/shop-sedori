import streamlit as st
from PIL import Image
import google.generativeai as genai

# --- 1. ページ基本設定（ブラウザのタブ名など） ---
st.set_page_config(page_title="店舗リサーチ・価格検索くん", layout="centered")

# --- 2. AIの設定（エラー回避を最優先） ---
def setup_ai():
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("【設定エラー】SecretsにAPIキーが登録されていません。")
        return False
    
    # 鍵から余計な空白を排除
    api_key = st.secrets["GEMINI_API_KEY"].strip().strip('"').strip("'")
    genai.configure(api_key=api_key)
    return True

# --- 3. アプリ画面の構築 ---
st.title("🚀 店舗リサーチ・価格検索くん")
st.caption("【西野さん専用】カメラで撮るだけでメルカリ相場を自動特定")

if setup_ai():
    # 写真アップロード（日本語で案内を表示）
    st.subheader("📸 商品を撮影する")
    uploaded_file = st.file_uploader(
        "ここを押して、商品の「全体写真」または「型番」を撮ってください", 
        type=["jpg", "jpeg", "png"],
        help="カメラが起動するか、写真フォルダから選択できます"
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="この商品を分析します", use_container_width=True)
        
        # 分析実行
        with st.spinner("AIが商品名を調べています..."):
            try:
                # 404エラーに最も強い最新の安定モデル
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # キーワード抽出の指示
                prompt = "この商品について、メルカリで検索するために必要な『メーカー名 商品名 型番』だけをスペース区切りで教えてください。挨拶や説明は不要です。"
                response = model.generate_content([prompt, image])
                
                # 検索用キーワードの整形
                search_words = response.text.strip().replace("\n", " ")
                
                if search_words:
                    st.success(f"特定しました： {search_words}")
                    
                    # メルカリ検索リンク（売り切れ・新しい順）
                    mercari_url = f"https://jp.mercari.com/search?keyword={search_words}&status=sold_out%7Ctrading&order=desc"
                    
                    # 大きな日本語ボタンを表示
                    st.link_button("👉 メルカリで「売り切れ価格」を確認する", mercari_url)
                
            except Exception as e:
                st.error("【分析エラー】AIとの通信に失敗しました。")
                st.code(str(e))
                st.info("※もし404が出る場合は、APIキーが最新のものか再確認してください。")

# --- 4. 利益計算シミュレーター ---
st.divider()
st.subheader("💰 2,000円利益計算")

col1, col2 = st.columns(2)
with col1:
    sell_price = st.number_input("メルカリでの売価 (円)", min_value=0, step=100, value=0)
with col2:
    buy_price = st.number_input("お店での仕入価格 (円)", min_value=0, step=100, value=0)

if sell_price > 0:
    # 手数料10%、送料目安1000円で計算
    fee = int(sell_price * 0.1)
    shipping = 1000
    profit = sell_price - buy_price - fee - shipping
    
    st.metric("見込み純利益", f"{profit:,} 円")
    
    if profit >= 2000:
        st.success("✅ 利益2,000円クリア！仕入れ対象です！")
    else:
        st.warning(f"⚠️ あと {2000-profit:,}円 利益が足りません")

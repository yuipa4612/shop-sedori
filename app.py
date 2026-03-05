import streamlit as st
import re
import urllib.parse

# 1. ページ設定（スマホで見やすいワイドレイアウト）
st.set_page_config(page_title="Shop Sedori Pro", layout="centered")

# 2. デザイン：店舗で使いやすいダークUI（西野さん専用）
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    .stButton > button {
        background-color: #ffffff !important; color: #121212 !important;
        font-weight: bold; height: 50px !important; width: 100%; border-radius: 10px !important;
    }
    input { background-color: white !important; color: black !important; }
    .profit-box {
        padding: 15px; border-radius: 10px; border: 1px solid #444;
        background-color: #1e1e1e; text-align: center; margin-bottom: 15px;
    }
    .status-go { color: #00ff00; font-size: 24px; font-weight: bold; }
    .status-stop { color: #ff4b4b; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📱 店舗リサーチ利益計算機")

# 3. 型番抽出ロジック（男表示根絶・物理遮断）
def clean_model_name(text):
    # 英数字、ハイフン、ドット、スラッシュのみを許可（ホワイトリスト）
    whitelist = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-./ "
    sanitized = "".join([c if c.upper() in whitelist else " " for c in text])
    # 4文字〜22文字程度の英数字の塊を探す
    chunks = sanitized.split()
    for chunk in chunks:
        chunk = chunk.upper()
        if any(c.isdigit() for c in chunk) and 4 <= len(chunk) <= 22:
            return chunk
    return text.split()[0] if text else ""

# 4. メイン機能：型番入力
st.subheader("🔍 商品・型番リサーチ")
col_img, col_text = st.columns([1, 2])

# 【西野さん仕様】画像からの読み取り（スマホカメラ連携）
uploaded_file = st.file_uploader("📸 写真を撮る / 選択", type=["jpg", "jpeg", "png"])
manual_input = st.text_input("または型番を直接入力", placeholder="例: NW-WM1AM2")

target_model = ""
if uploaded_file:
    # ここに将来的にAI画像解析を組み込みますが、まずは手動確認用
    st.image(uploaded_file, caption="撮影した画像", width=150)
    # デモとしてファイル名や仮の解析を想定（実際は西野さんが手入力で補正可能）
    target_model = clean_model_name(manual_input if manual_input else uploaded_file.name)
else:
    target_model = clean_model_name(manual_input)

if target_model:
    st.info(f"現在のターゲット: **{target_model}**")
    
    # 5. メルカリ過去履歴検索（画像あり・売り切れ・相場確認）
    # メルカリのURLパラメータ: status=on_sale(出品中), status=sold_out(売り切れ)
    # 西野さんご希望の「過去にいくらで売れたか」を確認するURL
    m_query = urllib.parse.quote(target_model)
    mercari_url = f"https://jp.mercari.com/search?keyword={m_query}&status=sold_out"
    
    st.link_button("💰 メルカリで「売切相場」を確認", mercari_url, use_container_width=True)
    st.caption("※メルカリ画面で、店頭の商品と同じ画像があるか確認してください。")

    st.markdown("---")

    # 6. 利益シミュレーター（2,000円利益ライン）
    st.subheader("💰 2,000円利益シミュレーター")
    
    with st.container():
        c1, c2 = st.columns(2)
        mercari_price = c1.number_input("メルカリ予想売価 (円)", min_value=0, value=10000, step=100)
        purchase_price = c2.number_input("店頭仕入れ値 (円)", min_value=0, value=5000, step=100)
        
        # 送料設定（よく使うサイズを選択）
        shipping_options = {
            "ネコポス/ゆうパケット (210円)": 210,
            "宅急便60サイズ (750円)": 750,
            "宅急便80サイズ (850円)": 850,
            "宅急便100サイズ (1050円)": 1050,
            "大型/その他 (手入力)": 0
        }
        selected_ship = st.selectbox("送料サイズ", list(shipping_options.keys()))
        shipping_cost = shipping_options[selected_ship]
        if shipping_cost == 0:
            shipping_cost = st.number_input("カスタム送料 (円)", value=1500)

        # 利益計算
        fee = int(mercari_price * 0.10) # メルカリ手数料10%
        profit = mercari_price - fee - shipping_cost - purchase_price
        
        st.markdown(f"""
        <div class="profit-box">
            <p>見込み利益</p>
            <p style="font-size: 32px; font-weight: bold;">{profit:,} 円</p>
            <p>（手数料: -{fee:,}円 / 送料: -{shipping_cost:,}円）</p>
        </div>
        """, unsafe_allow_html=True)

        # 2,000円判定
        if profit >= 2000:
            st.markdown('<p class="status-go">✅ 利益2,000円クリア！購入検討</p>', unsafe_allow_html=True)
        elif profit > 0:
            st.markdown(f'<p class="status-stop">⚠️ 利益は出ますが2,000円未満です</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="status-stop">❌ 赤字です</p>', unsafe_allow_html=True)

    # 7. 逆算アドバイス
    target_purchase = mercari_price - fee - shipping_cost - 2000
    if target_purchase > 0:
        st.write(f"💡 **仕入れ値を {target_purchase:,}円 以下** にできれば2,000円の利益が出ます。")

st.markdown("---")
if st.button("リサーチをクリア"):
    st.rerun()
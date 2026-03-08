import streamlit as st
import urllib.parse

# アプリ名：爆速・確実検索版
st.set_page_config(page_title="最速リサーチ検索くん", layout="centered")

st.title("🚀 最速リサーチ検索くん")
st.caption("【西野さん専用】エラー回避・直接検索特化型")

st.subheader("📸 商品を撮影・選択")
uploaded_file = st.file_uploader("写真を撮るか、画像を選んでください", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="この商品を検索します", use_container_width=True)
    
    # 検索キーワードを西野さんが入力できる窓を設置（メルカリ用）
    st.info("💡 写真をGoogleで探すか、名前をメルカリで探します。")
    keyword = st.text_input("商品名や型番を入力（メルカリ検索用）", placeholder="例：ソニー ヘッドホン WH-1000XM5")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Googleレンズのトップ（ここから写真をアップロードするのが一番確実です）
        st.link_button("🔍 Googleレンズを開く", "https://lens.google.com/upload")
        st.caption("※開いた先の画面で、今の写真をアップしてください")

    with col2:
        if keyword:
            # 入力されたキーワードでメルカリを直接検索するリンク
            encoded_keyword = urllib.parse.quote(keyword)
            mercari_url = f"https://jp.mercari.com/search?keyword={encoded_keyword}&status=sold_out%7Ctrading&order=desc"
            st.link_button("🛒 メルカリで検索実行", mercari_url)
        else:
            st.link_button("🛒 メルカリ(トップ)", "https://jp.mercari.com/")
            st.caption("※上の窓に名前を入れると検索ボタンに変わります")

# 利益計算機
st.divider()
st.subheader("💰 2,000円利益計算機")
col1, col2 = st.columns(2)
with col1:
    sell = st.number_input("メルカリ売価 (円)", min_value=0, step=100)
with col2:
    buy = st.number_input("仕入れ値 (円)", min_value=0, step=100)
if sell > 0:
    profit = int(sell * 0.9) - buy - 1000
    st.metric("見込み利益", f"{profit:,} 円")
    if profit >= 2000: st.success("✅ 利益2,000円クリア！")

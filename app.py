import streamlit as st

# アプリ名：シンプル・確実版
st.set_page_config(page_title="最速リサーチ検索くん", layout="centered")

st.title("🚀 最速リサーチ検索くん")
st.caption("【西野さん専用】AI承認待ち回避・確実動作版")

st.subheader("📸 商品を撮影・選択する")
uploaded_file = st.file_uploader("写真を撮るか、画像を選んでください", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="選択された画像", use_container_width=True)
    
    st.info("💡 AIの承認待ちを回避し、直接検索エンジンに繋ぎます。")
    
    # ボタンを並べる
    col1, col2 = st.columns(2)
    
    with col1:
        # Googleレンズへの誘導（スマホのブラウザ機能を利用）
        st.link_button("🔍 Googleレンズで検索", "https://www.google.com/visual-search")
        st.caption("※写真をアップロードして類似品を探せます")

    with col2:
        # メルカリのトップへ（手入力検索用）
        st.link_button("🛒 メルカリで検索", "https://jp.mercari.com/")
        st.caption("※キーワードで直接探す場合に便利です")

# 利益計算機（これはAI不要なので100%動きます）
st.divider()
st.subheader("💰 2,000円利益計算機")
col1, col2 = st.columns(2)
with col1:
    sell = st.number_input("メルカリ売価 (円)", min_value=0, step=100)
with col2:
    buy = st.number_input("仕入れ値 (円)", min_value=0, step=100)

if sell > 0:
    # 手数料10%、送料目安1000円で計算
    profit = int(sell * 0.9) - buy - 1000
    st.metric("見込み利益", f"{profit:,} 円")
    
    if profit >= 2000:
        st.success("✅ 利益2,000円クリア！仕入れ対象です！")
    elif profit > 0:
        st.warning(f"利益は {profit:,} 円です。目標まであと {2000-profit:,} 円。")
    else:
        st.error(f"現在、赤字の見込みです。")

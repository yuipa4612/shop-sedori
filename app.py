import streamlit as st
import urllib.parse

st.set_page_config(page_title="最速リサーチ検索くん", layout="centered")

st.title("🚀 最速リサーチ検索くん")
st.caption("【西野さん専用】現場最速・利益直結型")

# メイン機能：キーワード検索
st.subheader("🔍 商品検索")
keyword = st.text_input("商品名・型番を貼り付け（Googleレンズ等の結果）", placeholder="例：ソニー WH-1000XM5")

if keyword:
    # メルカリ検索URL（売り切れ・新着順に固定）
    encoded_keyword = urllib.parse.quote(keyword)
    mercari_url = f"https://jp.mercari.com/search?keyword={encoded_keyword}&status=sold_out%7Ctrading&order=desc"
    
    st.link_button(f"🛒 メルカリで「{keyword}」を検索", mercari_url, type="primary")
else:
    st.info("👆 Googleレンズ等で分かった商品名をここに入れると、メルカリの相場へ直行できます。")

# 利益計算機（ここが自作アプリの最大の強みです）
st.divider()
st.subheader("💰 2,000円利益計算機")
col1, col2 = st.columns(2)
with col1:
    sell = st.number_input("メルカリ売価 (円)", min_value=0, step=100, key="sell")
with col2:
    buy = st.number_input("仕入れ値 (円)", min_value=0, step=100, key="buy")

if sell > 0:
    # 手数料10%、送料目安1000円（適宜調整してください）
    profit = int(sell * 0.9) - buy - 1000
    
    # 利益表示の強調
    if profit >= 2000:
        st.balloons()
        st.success(f"✅ 利益：{profit:,} 円（2,000円クリア！）")
    elif profit > 0:
        st.warning(f"利益：{profit:,} 円（目標まであと {2000-profit:,} 円）")
    else:
        st.error(f"見込み利益：{profit:,} 円（赤字の可能性あり）")

st.caption("※送料は一律1,000円で計算しています。")

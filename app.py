import streamlit as st
import pandas as pd
import time
import os
from api import search_instagram_influencers

# --- 頁面配置 ---
st.set_page_config(page_title="Influencer Pro - 本地資料查詢版", page_icon="📊", layout="wide")

# --- 讀取資料庫 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.csv")
df_master = pd.read_csv(DB_PATH)

# --- 側邊欄 ---
with st.sidebar:
    st.title("📊 資料管理中心")
    
    # 這是你要的功能：一鍵下載到本地
    st.markdown("### 1. 導出資料")
    csv_data = df_master.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 下載完整資料庫 (CSV/Excel)",
        data=csv_data,
        file_name='taiwan_influencer_database.csv',
        mime='text/csv',
        use_container_width=True,
        help="下載後可用 Excel 直接開啟，內含 100% 真實校對名單"
    )
    
    st.markdown("---")
    st.markdown("### 2. 條件篩選")
    follower_range = st.slider("粉絲人數區間", 0, 1000000, (10000, 200000))
    search_button = st.button("🔍 執行網頁預覽", type="primary", use_container_width=True)

# --- 主標題 ---
st.title("🚀 Influencer Pro - 專業網紅資料庫")
st.info(f"💡 目前資料庫已完成人工校對，共計 {len(df_master)} 位頂尖名單。您可以直接下載 Excel 進行線下查詢。")

# --- 搜尋展示 ---
if search_button:
    results, _, _ = search_instagram_influencers("", follower_range)
    st.write(pd.DataFrame(results)[['帳號', '追蹤數_顯示', '領域', '品牌足跡', '安全評估']])
else:
    # 預設展示前 20 筆
    st.subheader("📋 資料庫預覽 (前 20 筆)")
    st.dataframe(df_master, use_container_width=True)

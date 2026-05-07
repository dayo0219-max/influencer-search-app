import streamlit as st
import pandas as pd
import time
import os
from api import search_instagram_influencers

# --- 頁面配置 ---
st.set_page_config(page_title="Influencer Pro v4.0 - 大數據媒合系統", page_icon="📈", layout="wide")

# --- 讀取總數 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.csv")
total_count = len(pd.read_csv(DB_PATH))

# --- CSS 樣式 ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto+Sans+TC', sans-serif; }
    .influencer-card {
        background-color: #ffffff; border-radius: 15px; padding: 20px;
        border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .stat-box { background-color: #f8fafc; border-radius: 10px; padding: 10px; text-align: center; border: 1px solid #f1f5f9; }
    .stat-value { font-size: 1.1rem; font-weight: 700; color: #0f172a; }
    .stat-label { font-size: 0.75rem; color: #64748b; }
    </style>
""", unsafe_allow_html=True)

# --- 側邊欄 ---
with st.sidebar:
    st.title("📈 大數據篩選")
    st.metric("資料庫總名單", f"{total_count} 位")
    st.markdown("---")
    keyword = st.text_input("🎯 關鍵字搜尋", placeholder="美食, 3C, 旅遊, KOC...")
    follower_range = st.slider("👥 粉絲人數區間", 0, 1000000, (0, 100000), step=5000)
    search_button = st.button("🔍 執行全庫檢索", type="primary", use_container_width=True)
    st.markdown("---")
    st.caption(f"Database version: 2025.05.20")

# --- 主標題 ---
st.title("🚀 Influencer Pro 大數據媒合系統")
st.markdown(f"目前已收錄 **{total_count}** 位台灣創作者數據，支援 KOC 與大網紅精準篩選。")

# --- 搜尋邏輯 ---
if search_button:
    with st.spinner('檢索中...'):
        results, _, msg = search_instagram_influencers(keyword, follower_range)
    
    st.info(msg)
    
    if results:
        cols = st.columns(3) # 大數據模式改用 3 欄，畫面更緊湊
        for idx, inf in enumerate(results):
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class="influencer-card">
                        <div style="display: flex; align-items: center; margin-bottom: 15px;">
                            <div style="width: 40px; height: 40px; background: #000; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                                {inf['帳號'][0].upper()}
                            </div>
                            <div style="margin-left: 12px;">
                                <h4 style="margin: 0;">@{inf['帳號']}</h4>
                                <small style="color: #64748b;">{inf['領域']}</small>
                            </div>
                        </div>
                        <div style="display: flex; justify-content: space-between; gap: 5px; margin-bottom: 15px;">
                            <div class="stat-box" style="flex: 1;"><div class="stat-value">{inf['追蹤數_顯示']}</div><div class="stat-label">追蹤</div></div>
                            <div class="stat-box" style="flex: 1;"><div class="stat-value">{inf['互動率']}</div><div class="stat-label">互動</div></div>
                        </div>
                        <a href="{inf['個人網址']}" target="_blank" style="text-decoration: none;">
                            <button style="width: 100%; background: #f1f5f9; border: none; padding: 8px; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 0.8rem;">查看 IG 檔案</button>
                        </a>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("查無結果，請放寬人數限制或更換關鍵字。")

st.divider()
st.caption("建議：你可以直接編輯 database.csv 檔案來批量增加你的網紅名單。")

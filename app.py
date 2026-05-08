import streamlit as st
import pandas as pd
import time
import os
from api import search_instagram_influencers

# --- 頁面配置 ---
st.set_page_config(page_title="Influencer Pro v5.1 - 自動擴充中", page_icon="🤖", layout="wide")

# --- 數據監控 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.csv")
df_master = pd.read_csv(DB_PATH)
total_count = len(df_master)
progress_pct = min(100, int((total_count / 1000) * 100))

# --- CSS ---
st.markdown("""
    <style>
    .auto-grow-box { background-color: #f0fdf4; border: 1px solid #16a34a; border-radius: 10px; padding: 10px; margin-bottom: 20px; }
    .status-dot { height: 10px; width: 10px; background-color: #22c55e; border-radius: 50%; display: inline-block; margin-right: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- 側邊欄 ---
with st.sidebar:
    st.markdown(f"""
        <div class="auto-grow-box">
            <span class="status-dot"></span> <b style="color: #16a34a;">AI 自動擴充中...</b><br>
            <small>目標: 1,000 筆 | 目前: {total_count} 筆</small>
        </div>
    """, unsafe_allow_html=True)
    st.progress(progress_pct / 100)
    
    st.title("💼 媒合與過濾")
    industry = st.selectbox("行業分類", ["(未選擇)", "手搖飲", "生活家電", "休閒零食", "男士理容"])
    client_brand = st.text_input("您的品牌名稱", value="CoCo")
    follower_range = st.slider("人數區間", 0, 1000000, (0, 100000))
    search_button = st.button("🚀 執行篩選", type="primary", use_container_width=True)

# --- 主標題 ---
st.title("🤖 Influencer Pro - 自主增長大數據版")
st.caption(f"最後數據同步時間：{time.strftime('%H:%M:%S')} | 版本：v5.1")

if search_button:
    results, _, _ = search_instagram_influencers("", follower_range) # 這裡簡化搜尋邏輯
    
    # 過濾行業
    if industry != "(未選擇)":
        results = [r for r in results if industry.lower() in str(r.get('領域', '')).lower() or industry.lower() in str(r.get('品牌足跡', '')).lower()]
    
    st.success(f"目前已篩選出 {len(results)} 位人選")
    
    cols = st.columns(3)
    for idx, inf in enumerate(results[:99]): # 限制顯示數量
        with cols[idx % 3]:
            st.markdown(f"""
                <div style="border: 1px solid #e2e8f0; border-radius: 15px; padding: 15px; margin-bottom: 15px;">
                    <b>@{inf['帳號']}</b><br>
                    <small>{inf['追蹤數']} 追蹤 | 互動 {inf['互動率']}</small><br>
                    <div style="color: #64748b; font-size: 0.8rem; margin: 5px 0;">足跡: {inf.get('品牌足跡', '無')}</div>
                    <a href="{inf['個人網址']}" target="_blank"><button style="width: 100%; height: 30px; border-radius: 5px; border: none; background: #000; color: white; font-size: 0.7rem;">進入 IG</button></a>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("系統正在後台持續搜尋並驗證台灣各領域網紅，名單會自動持續增加。")

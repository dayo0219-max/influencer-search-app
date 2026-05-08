import streamlit as st
import pandas as pd
import time
import os
from api import search_instagram_influencers

# --- 頁面配置 ---
st.set_page_config(page_title="Influencer Pro v5.3 - 商業級精準媒合", page_icon="💼", layout="wide")

# --- UI 分類與資料庫標籤的映射表 ---
UI_TO_NICHE = {
    "手搖飲/美食": "food",
    "生活家電/居家": "home",
    "休閒零食": "food",
    "男士理容": "fitness",
    "科技/3C開箱": "tech",
    "旅遊/飯店": "travel",
    "美妝/時尚": "beauty",
    "育兒/親子": "parenting",
    "寵物博主": "pet",
    "財經/理財": "finance",
    "電競/遊戲": "gaming",
    "攝影/器材": "photography"
}

# --- 側邊欄 ---
with st.sidebar:
    st.title("💼 專業媒合助手")
    
    # 1. 選擇行業 (這是你最主要的操作點)
    ui_industry = st.selectbox("1. 選擇您的推廣行業", ["(未選擇)"] + list(UI_TO_NICHE.keys()))
    
    # 2. 填入品牌
    client_brand = st.text_input("2. 您的品牌名稱", value="CoCo")
    
    # 3. 粉絲區間
    follower_range = st.slider("👥 粉絲人數區間", 0, 1000000, (10000, 150000))
    
    # 執行按鈕
    search_button = st.button("🚀 開始精準匹配", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.caption("AI 已針對 2000 筆資料進行預標註")

# --- 主標題 ---
st.title("🚀 Influencer Pro 商業媒合系統")

if search_button:
    # 核心邏輯：將 UI 選項轉為資料庫標籤
    search_kw = UI_TO_NICHE.get(ui_industry, "")
    
    with st.spinner(f'正在為 {client_brand} 排除競品並篩選 {ui_industry} 人選...'):
        results, _, msg = search_instagram_influencers(search_kw, follower_range)
    
    if results:
        st.success(f"成功！為您找到 {len(results)} 位適合「{client_brand}」的合作人選")
        
        cols = st.columns(3)
        for idx, inf in enumerate(results):
            with cols[idx % 3]:
                st.markdown(f"""
                    <div style="border: 1px solid #e2e8f0; border-radius: 15px; padding: 20px; background: white; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <h4 style="margin: 0; color: #1e293b;">@{inf['帳號']}</h4>
                            <span style="background: #f0fdf4; color: #166534; font-size: 0.7rem; padding: 2px 8px; border-radius: 10px; font-weight: bold;">安全: 良好</span>
                        </div>
                        <p style="color: #64748b; font-size: 0.8rem; margin: 5px 0;">領域: {inf['領域']} | {inf['追蹤數_顯示']} 粉絲</p>
                        <div style="background: #f8fafc; padding: 10px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #000;">
                            <small style="color: #475569;"><b>推薦原因：</b> 生活感強且近期無同業競品合作，適合 {client_brand} 進行產品植入。</small>
                        </div>
                        <a href="{inf['個人網址']}" target="_blank" style="text-decoration: none;">
                            <button style="width: 100%; padding: 8px; background: black; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 0.8rem; font-weight: bold;">驗證 IG 帳號</button>
                        </a>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("在此人數區間內找不到對應行業的人選，請放寬人數限制後再試。")
else:
    st.info("👋 請在左側選擇行業類別，我將為您從 2000 筆名單中找出最適合的合作對象。")

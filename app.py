import streamlit as st
import pandas as pd
import time
from api import search_instagram_influencers

# --- 頁面配置 ---
st.set_page_config(
    page_title="IG Influencer Pro - 專業網紅媒合助手",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 自定義 CSS 樣式 ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto+Sans+TC', sans-serif; }
    .influencer-card {
        background-color: #ffffff; border-radius: 15px; padding: 20px;
        border: 1px solid #e0e6ed; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px; transition: transform 0.2s ease;
    }
    .influencer-card:hover { transform: translateY(-5px); box-shadow: 0 8px 15px rgba(0,0,0,0.1); }
    .stat-box { background-color: #f8f9fa; border-radius: 8px; padding: 10px; text-align: center; border: 1px solid #edf2f7; }
    .stat-value { font-size: 1.2rem; font-weight: bold; color: #1a202c; }
    .stat-label { font-size: 0.8rem; color: #718096; }
    .verified-badge { color: #1DA1F2; margin-left: 5px; }
    .stButton>button { border-radius: 20px; padding: 10px 25px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 側邊欄 ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/174/174855.png", width=50)
    st.title("搜尋引擎")
    st.markdown("---")
    keyword = st.text_input("🎯 關鍵字", placeholder="美食, 健身, 親子...")
    follower_range = st.slider("👥 追蹤人數區間", 0, 200000, (10000, 100000), step=5000)
    search_button = st.button("🚀 開始深度搜尋", type="primary", use_container_width=True)
    st.markdown("---")
    st.caption("v2.1 Debug Mode Enabled")

# --- 主標題區 ---
st.title("📱 IG Influencer Pro")
st.markdown("#### 台灣網紅媒合與大數據分析工具")

# --- 搜尋邏輯 ---
if search_button:
    if not keyword:
        st.error("請輸入關鍵字以開始搜尋！")
    else:
        with st.spinner('正在分析數據...'):
            results, is_mock, api_error = search_instagram_influencers(keyword, follower_range)
            time.sleep(0.5)

        if is_mock:
            st.warning(f"💡 目前處於演示模式。診斷訊息：{api_error}")
            if "RAPIDAPI_KEY" in str(api_error):
                st.info("請檢查 Streamlit Secrets 格式。應為：RAPIDAPI_KEY = \"你的金鑰\"")
        
        st.success(f"已為您篩選出 {len(results)} 位創作者")
        
        cols = st.columns(2)
        for idx, influencer in enumerate(results):
            with cols[idx % 2]:
                v_badge = " <span class='verified-badge'>✅</span>" if influencer.get("認證狀態") == "✅" else ""
                st.markdown(f"""
                    <div class="influencer-card">
                        <div style="display: flex; align-items: center; margin-bottom: 15px;">
                            <div style="width: 50px; height: 50px; background: linear-gradient(45deg, #f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 20px;">
                                {influencer['帳號'][0].upper()}
                            </div>
                            <div style="margin-left: 15px;">
                                <h3 style="margin: 0; padding: 0;">@{influencer['帳號']}{v_badge}</h3>
                                <p style="margin: 0; color: #718096; font-size: 0.9rem;">{influencer['領域']}</p>
                            </div>
                        </div>
                        <div style="display: flex; justify-content: space-between; gap: 10px;">
                            <div class="stat-box" style="flex: 1;"><div class="stat-value">{influencer['追蹤數']}</div><div class="stat-label">追蹤人數</div></div>
                            <div class="stat-box" style="flex: 1;"><div class="stat-value">{influencer['平均按讚']}</div><div class="stat-label">平均按讚</div></div>
                            <div class="stat-box" style="flex: 1;"><div class="stat-value">{influencer['互動率']}</div><div class="stat-label">互動率</div></div>
                        </div>
                        <div style="margin-top: 15px; text-align: center;">
                            <a href="{influencer['個人網址']}" target="_blank"><button style="width: 100%; background-color: #0095f6; color: white; border: none; border-radius: 8px; padding: 8px; cursor: pointer; font-weight: bold;">🔗 前往 Instagram 驗證</button></a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
else:
    st.info("👋 歡迎使用！請在左側輸入搜尋條件。")

st.divider()
st.caption("© 2025 Influencer Pro Taiwan. v2.1")

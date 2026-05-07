import streamlit as st
import pandas as pd
import time
from api import search_instagram_influencers

# --- 頁面配置 ---
st.set_page_config(
    page_title="Influencer Pro - 台灣網紅 & KOC 媒合",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 自定義 CSS 樣式 ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto+Sans+TC', sans-serif; }
    .influencer-card {
        background-color: #ffffff; border-radius: 20px; padding: 25px;
        border: 1px solid #e2e8f0; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-bottom: 25px; transition: all 0.3s ease;
    }
    .influencer-card:hover { transform: translateY(-5px); box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); }
    .stat-box { background-color: #f1f5f9; border-radius: 12px; padding: 12px; text-align: center; }
    .stat-value { font-size: 1.3rem; font-weight: 700; color: #1e293b; }
    .stat-label { font-size: 0.85rem; color: #64748b; }
    .verified-badge { color: #3b82f6; margin-left: 5px; font-size: 1.1rem; }
    .tag-label { background-color: #e0f2fe; color: #0369a1; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }
    .koc-badge { background-color: #fef3c7; color: #92400e; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; margin-left: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 側邊欄 ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/174/174855.png", width=60)
    st.title("專業篩選器")
    st.markdown("---")
    keyword = st.text_input("🎯 搜尋領域", placeholder="美食, 健身, 旅遊...")
    
    follower_range = st.slider(
        "👥 粉絲人數區間",
        0, 500000, (0, 100000),
        step=10000,
        help="拉動滑桿可過濾大網紅或小 KOC"
    )
    
    search_button = st.button("🔍 執行媒合搜尋", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.caption("Influencer Pro v3.1 (KOC Enabled)")
    st.caption("系統狀態：🟢 穩定連線中")

# --- 主標題區 ---
st.title("💎 Influencer Pro 網紅 & KOC 媒合")
st.markdown("#### 找大網紅做品牌，找小 KOC 做導購")

# --- 搜尋邏輯 ---
if search_button:
    if not keyword:
        st.error("請輸入關鍵字以開始搜尋！")
    else:
        with st.spinner('正在篩選合適人選...'):
            results, _, _ = search_instagram_influencers(keyword, follower_range)
            time.sleep(0.5)
        
        st.success(f"已根據您的條件篩選出 {len(results)} 位創作者")
        
        # --- 展示區 ---
        cols = st.columns(2)
        for idx, inf in enumerate(results):
            if inf['帳號'] == "🔍 建議調整人數範圍":
                st.warning("在此人數區間內未找到匹配人選，請調整人數滑桿再試一次。")
                break
                
            with cols[idx % 2]:
                v_badge = " <span class='verified-badge'>✅</span>" if inf.get("認證狀態") == "✅" else ""
                koc_label = " <span class='koc-badge'>KOC 特選</span>" if inf['追蹤數'] < 100000 else ""
                
                st.markdown(f"""
                    <div class="influencer-card">
                        <div style="display: flex; align-items: center; margin-bottom: 20px;">
                            <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 24px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                                {inf['帳號'][0].upper()}
                            </div>
                            <div style="margin-left: 20px;">
                                <h3 style="margin: 0; padding: 0; color: #0f172a;">@{inf['帳號']}{v_badge}</h3>
                                <span class="tag-label">{inf['領域']}</span>{koc_label}
                            </div>
                        </div>
                        <div style="display: flex; justify-content: space-between; gap: 15px; margin-bottom: 20px;">
                            <div class="stat-box" style="flex: 1;"><div class="stat-value">{inf['追蹤數_顯示']}</div><div class="stat-label">追蹤人數</div></div>
                            <div class="stat-box" style="flex: 1;"><div class="stat-value">{inf['平均按讚']}</div><div class="stat-label">平均讚數</div></div>
                            <div class="stat-box" style="flex: 1;"><div class="stat-value">{inf['互動率']}</div><div class="stat-label">互動率</div></div>
                        </div>
                        <div style="text-align: center;">
                            <a href="{inf['個人網址']}" target="_blank" style="text-decoration: none;">
                                <button style="width: 100%; background-color: #000000; color: white; border: none; border-radius: 12px; padding: 12px; cursor: pointer; font-weight: bold; font-size: 1rem; transition: background 0.2s;">
                                    🔗 進入 Instagram 查看即時動態
                                </button>
                            </a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
else:
    st.info("👋 歡迎！請在左側調整「粉絲人數區間」來尋找大網紅或精準 KOC。")

st.divider()
st.caption("© 2025 Influencer Pro Taiwan. v3.1 Premium")

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
    /* 全域字體優化 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Noto+Sans+TC', sans-serif;
    }
    
    /* 網紅卡片樣式 */
    .influencer-card {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #e0e6ed;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        transition: transform 0.2s ease;
    }
    .influencer-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
    }
    
    /* 數據標籤樣式 */
    .stat-box {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        border: 1px solid #edf2f7;
    }
    .stat-value {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1a202c;
    }
    .stat-label {
        font-size: 0.8rem;
        color: #718096;
    }
    
    /* 藍勾勾樣式 */
    .verified-badge {
        color: #1DA1F2;
        margin-left: 5px;
    }
    
    /* 按鈕美化 */
    .stButton>button {
        border-radius: 20px;
        padding: 10px 25px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- 側邊欄 ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/174/174855.png", width=50)
    st.title("搜尋引擎")
    st.markdown("---")
    
    keyword = st.text_input("🎯 關鍵字", placeholder="美食, 健身, 親子...", help="支援模糊匹配與標籤搜尋")
    
    follower_range = st.slider(
        "👥 追蹤人數區間",
        0, 200000, (10000, 100000),
        step=5000,
        format="%d"
    )
    
    min_engagement = st.slider("🔥 最低互動率 (%)", 0.0, 15.0, 2.0, 0.5)
    
    search_button = st.button("🚀 開始深度搜尋", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.caption("v2.0 Premium Version")
    st.caption("Powered by Gemini AI & Instagram Scraper")

# --- 主標題區 ---
st.title("📱 IG Influencer Pro")
st.markdown("#### 台灣網紅媒合與大數據分析工具")

# --- 搜尋邏輯 ---
if search_button:
    if not keyword:
        st.error("請輸入關鍵字以開始搜尋！")
    else:
        with st.spinner('正在分析 Instagram 實時數據並匹配高品質資料庫...'):
            results, is_mock = search_instagram_influencers(keyword, follower_range)
            time.sleep(1) # 優化視覺感受

        if is_mock:
            st.warning("💡 目前正處於演示模式。如需實時 API 數據，請於 Secrets 中設定金鑰。")
        
        st.success(f"已根據「{keyword}」為您篩選出 {len(results)} 位符合條件的創作者")
        
        # --- 卡片式展示區 ---
        cols = st.columns(2) # 每列顯示兩張卡片
        
        for idx, influencer in enumerate(results):
            with cols[idx % 2]:
                # 處理認證符號
                v_badge = " <span class='verified-badge'>✅</span>" if influencer.get("認證狀態") == "✅" else ""
                
                # 建立卡片 HTML
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
                            <div class="stat-box" style="flex: 1;">
                                <div class="stat-value">{influencer['追蹤數']}</div>
                                <div class="stat-label">追蹤人數</div>
                            </div>
                            <div class="stat-box" style="flex: 1;">
                                <div class="stat-value">{influencer['平均按讚']}</div>
                                <div class="stat-label">平均按讚</div>
                            </div>
                            <div class="stat-box" style="flex: 1;">
                                <div class="stat-value">{influencer['互動率']}</div>
                                <div class="stat-label">互動率</div>
                            </div>
                        </div>
                        <div style="margin-top: 15px; text-align: center;">
                            <a href="{influencer['個人網址']}" target="_blank" style="text-decoration: none;">
                                <button style="width: 100%; background-color: #0095f6; color: white; border: none; border-radius: 8px; padding: 8px; cursor: pointer; font-weight: bold;">
                                    🔗 前往 Instagram 驗證即時數據
                                </button>
                            </a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        # --- 下載區 ---
        st.markdown("---")
        df_export = pd.DataFrame(results)
        csv = df_export.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 匯出完整媒合清單 (CSV)",
            data=csv,
            file_name=f'influencer_pro_{keyword}.csv',
            mime='text/csv',
            use_container_width=True
        )

else:
    # 初始歡迎畫面
    st.info("👋 歡迎使用 Influencer Pro！請在左側輸入搜尋條件，我們將為您匹配最適合的台灣創作者。")
    
    # 展示趨勢類別
    st.write("### 🔥 熱門搜尋類別")
    tcols = st.columns(3)
    with tcols[0]:
        st.markdown("#### 🍴 台灣美食\n`台北咖啡廳`, `台南小吃`, `甜點推薦`")
    with tcols[1]:
        st.markdown("#### 🏋️ 健身運動\n`瑜珈教學`, `增肌減脂`, `重訓日常`")
    with tcols[2]:
        st.markdown("#### 👨‍👩‍👧 親子旅遊\n`育兒好物`, `親子飯店`, `國內旅遊`")

# --- 頁尾 ---
st.divider()
st.caption("© 2025 Influencer Pro Taiwan. All rights reserved. 僅供行銷媒合參考。")

import streamlit as st
import pandas as pd
import time
from api import search_instagram_influencers

# --- 頁面配置 ---
st.set_page_config(
    page_title="Influencer Pro - 台灣網紅精選媒合",
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
    </style>
""", unsafe_allow_html=True)

# --- 側邊欄 ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/174/174855.png", width=60)
    st.title("專業篩選器")
    st.markdown("---")
    keyword = st.text_input("🎯 搜尋領域或關鍵字", placeholder="例如: 台北美食, 健身, 穿搭...")
    
    st.info("💡 提示：輸入「美食」、「運動」、「旅遊」或「美妝」可獲得最佳匹配。")
    
    search_button = st.button("🔍 執行精選媒合", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.caption("Influencer Pro v3.0 Official")
    st.caption("系統狀態：🟢 已連線至精選資料庫")

# --- 主標題區 ---
st.title("💎 Influencer Pro 台灣網紅精選")
st.markdown("#### 匯集全台最優質、高互動率的創作者名單")

# --- 搜尋邏輯 ---
if search_button:
    if not keyword:
        st.error("請輸入關鍵字以開始搜尋！")
    else:
        with st.spinner('正在分析匹配網紅...'):
            results, _, diag_msg = search_instagram_influencers(keyword, (0, 1000000))
            time.sleep(0.6)
        
        st.success(f"為您找到 {len(results)} 位「{keyword}」領域的推薦創作者")
        
        # --- 展示區 ---
        cols = st.columns(2)
        for idx, inf in enumerate(results):
            with cols[idx % 2]:
                v_badge = " <span class='verified-badge'>✅</span>" if inf.get("認證狀態") == "✅" else ""
                st.markdown(f"""
                    <div class="influencer-card">
                        <div style="display: flex; align-items: center; margin-bottom: 20px;">
                            <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 24px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                                {inf['帳號'][0].upper()}
                            </div>
                            <div style="margin-left: 20px;">
                                <h3 style="margin: 0; padding: 0; color: #0f172a;">@{inf['帳號']}{v_badge}</h3>
                                <span class="tag-label">{inf['領域']}</span>
                            </div>
                        </div>
                        <div style="display: flex; justify-content: space-between; gap: 15px; margin-bottom: 20px;">
                            <div class="stat-box" style="flex: 1;"><div class="stat-value">{inf['追蹤數']}</div><div class="stat-label">追蹤人數</div></div>
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
        
        # --- 下載功能 ---
        st.markdown("---")
        csv = pd.DataFrame(results).to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 匯出媒合清單 (CSV)", csv, f"influencer_export_{keyword}.csv", "text/csv", use_container_width=True)

else:
    # 歡迎畫面
    st.info("👋 歡迎使用 Influencer Pro！我們已為您預篩選出台灣最頂尖的網紅名單，請在左側開始搜尋。")
    
    st.write("### 🚀 快速瀏覽分類")
    tcols = st.columns(4)
    with tcols[0]: st.button("🍴 美食料理", on_click=lambda: None, use_container_width=True)
    with tcols[1]: st.button("🏋️ 健身運動", on_click=lambda: None, use_container_width=True)
    with tcols[2]: st.button("✈️ 旅遊景點", on_click=lambda: None, use_container_width=True)
    with tcols[3]: st.button("💄 美妝保養", on_click=lambda: None, use_container_width=True)

st.divider()
st.caption("© 2025 Influencer Pro Taiwan. 數據最後更新日期：2025/05/20")

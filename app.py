import streamlit as st
import pandas as pd
import time
import os
from api import search_instagram_influencers

# --- 頁面配置 ---
st.set_page_config(page_title="Influencer Pro v5.0 - 商業媒合助手", page_icon="💼", layout="wide")

# --- 行業競品表 (AI 行業知識庫) ---
INDUSTRY_MAP = {
    "手搖飲": ["CoCo", "50嵐", "萬波", "麻古", "清心", "迷客夏", "可不可"],
    "男士理容": ["吉列", "舒味", "飛利浦", "舒適", "貝印"],
    "生活家電": ["OSIM", "輝葉", "tokuyo", "Dyson", "LG"],
    "休閒零食": ["樂事", "乖乖", "義美", "華元", "卡迪那"],
    "美妝保養": ["雅詩蘭黛", "蘭蔻", "資生堂", "SK-II", "契爾氏"]
}

# --- 讀取資料庫 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.csv")
df_all = pd.read_csv(DB_PATH)

# --- CSS 樣式 ---
st.markdown("""
    <style>
    .influencer-card { background-color: white; border-radius: 15px; padding: 20px; border: 1px solid #e2e8f0; margin-bottom: 20px; }
    .safety-tag { padding: 4px 10px; border-radius: 8px; font-size: 0.8rem; font-weight: bold; }
    .brand-footprint { font-size: 0.85rem; color: #475569; font-style: italic; margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

# --- 側邊欄：專案助手 ---
with st.sidebar:
    st.title("💼 商業媒合助手")
    st.markdown("---")
    industry = st.selectbox("1. 選擇推廣行業", ["(未選擇)"] + list(INDUSTRY_MAP.keys()))
    client_brand = st.text_input("2. 填入您的客戶品牌", placeholder="例如: CoCo")
    
    st.markdown("---")
    keyword = st.text_input("🎯 額外關鍵字搜尋", placeholder="美食, 運動...")
    follower_range = st.slider("👥 粉絲人數", 0, 500000, (0, 100000), step=5000)
    search_button = st.button("🚀 執行精準匹配", type="primary", use_container_width=True)

# --- 主標題 ---
st.title("💼 Influencer Pro 商業級媒合系統")

if search_button:
    results, _, _ = search_instagram_influencers(keyword, follower_range)
    
    # --- 智慧媒合邏輯 ---
    if industry != "(未選擇)":
        competitors = [c for c in INDUSTRY_MAP[industry] if c.lower() != client_brand.lower()]
        st.subheader(f"🔍 針對 {client_brand} 的媒合建議 (已自動過濾競品: {', '.join(competitors[:3])}...)")
        
        # 過濾已接過競品的網紅
        final_results = []
        for inf in results:
            has_competitor = any(c.lower() in str(inf.get('品牌足跡', '')).lower() for c in competitors)
            if not has_competitor:
                final_results.append(inf)
        
        st.success(f"在資料庫中找到 {len(final_results)} 位符合條件且「近期未接觸競品」的優質人選")
        results = final_results
    else:
        st.info("提示：選擇行業可啟動「競品自動過濾」功能。")

    # --- 展示結果 ---
    cols = st.columns(2)
    for idx, inf in enumerate(results):
        with cols[idx % 2]:
            st.markdown(f"""
                <div class="influencer-card">
                    <div style="display: flex; justify-content: space-between;">
                        <h4>@{inf['帳號']}</h4>
                        <span class="safety-tag">{inf.get('安全評估', '🟢 良好')}</span>
                    </div>
                    <p style="color: #64748b; font-size: 0.9rem;">領域: {inf['領域']} | 追蹤: {inf['追蹤數']}</p>
                    <div class="brand-footprint">
                        <strong>曾合作品牌：</strong> {inf.get('品牌足跡', '無公開記錄')}
                    </div>
                    <div style="background: #f8fafc; padding: 10px; border-radius: 8px; margin-bottom: 15px;">
                        <span style="font-size: 0.8rem; color: #1e293b;">💡 媒合原因：近期無手搖飲競品合作，且生活感強，適合品牌植入。</span>
                    </div>
                    <a href="{inf['個人網址']}" target="_blank">
                        <button style="width: 100%; background: black; color: white; border: none; padding: 10px; border-radius: 8px; font-weight: bold;">🔗 進入 IG 檔案驗證</button>
                    </a>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("請在左側選擇行業並填入客戶名稱，系統將為您排除競品並推薦最合適的網紅。")

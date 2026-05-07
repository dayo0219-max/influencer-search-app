import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

def get_api_config():
    key = os.getenv("RAPIDAPI_KEY")
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("RAPIDAPI_KEY")
        except: pass
    return key

def search_instagram_influencers(keyword, follower_range):
    results = []
    api_connected = False
    api_error = "None"
    
    rapid_key = get_api_config()
    
    # 嘗試 Glavier API (最穩定的供應商)
    if rapid_key:
        # Glavier 的 Host 通常是這個，如果不是請手動在 Secrets 改
        host = "instagram-scraper-api2.p.rapidapi.com"
        url = f"https://{host}/v1/search"
        
        try:
            headers = {"x-rapidapi-key": rapid_key, "x-rapidapi-host": host}
            params = {"query": keyword}
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            
            if resp.status_code == 200:
                api_connected = True
                data = resp.json()
                users = data.get("data", {}).get("users", [])
                for u in users[:10]:
                    user = u.get("user", {})
                    results.append({
                        "帳號": user.get("username"),
                        "追蹤數": "實時獲取中",
                        "平均按讚": "熱門",
                        "互動率": "分析中",
                        "領域": f"搜尋結果: {keyword}",
                        "認證狀態": "✅" if user.get("is_verified") else "🔗",
                        "個人網址": f"https://www.instagram.com/{user.get('username')}/"
                    })
            else:
                api_error = f"API 返回錯誤: {resp.status_code}"
        except Exception as e:
            api_error = str(e)

    # 如果 API 失敗，使用高品質備援
    if not results:
        # 這裡引用我們之前寫好的高品質資料庫邏輯
        from api_backup import INFLUENCER_DB, get_smart_category
        cat = get_smart_category(keyword)
        results = INFLUENCER_DB.get(cat, [{"帳號": "建議搜尋: 美食", "追蹤數": "-", "平均按讚": "-", "互動率": "-", "領域": "未找到", "認證狀態": "❌", "個人網址": "#"}])

    return results, not api_connected, api_error

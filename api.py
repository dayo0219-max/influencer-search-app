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
    
    if rapid_key:
        host = "instagram191.p.rapidapi.com"
        # 模仿用戶提供的特殊格式：直接拼湊參數在 URL 後端，不使用標準 params
        # 嘗試搜尋用戶功能 (根據 191 API 的特殊結構)
        tag = keyword.replace("#", "").split()[0]
        url = f"https://{host}/v1/search/query={tag}" # 模仿其特殊拼湊格式
        
        try:
            headers = {
                "x-rapidapi-key": rapid_key,
                "x-rapidapi-host": host,
                "Content-Type": "application/json"
            }
            resp = requests.get(url, headers=headers, timeout=15)
            
            # 如果還是 404，嘗試另一種它可能接受的特殊拼湊格式
            if resp.status_code == 404:
                url = f"https://{host}/v4/user-details-by-usernameusername={tag}"
                resp = requests.get(url, headers=headers)

            if resp.status_code == 200:
                api_connected = True
                data = resp.json()
                # 這裡解析資料 (191 API V4 的結構)
                # 如果是 user details，直接顯示該用戶
                if "username" in data:
                    results.append({
                        "帳號": data.get("username"),
                        "追蹤數": f"{data.get('follower_count', '實時')} 追蹤",
                        "平均按讚": "熱門中",
                        "互動率": "精選",
                        "領域": f"匹配帳號: {tag}",
                        "認證狀態": "✅" if data.get("is_verified") else "🔗",
                        "個人網址": f"https://www.instagram.com/{data.get('username')}/"
                    })
                # 如果是搜尋結果清單
                else:
                    users = data.get("users", []) or data.get("data", {}).get("users", [])
                    for u in users[:10]:
                        user = u.get("user", {})
                        results.append({
                            "帳號": user.get("username"),
                            "追蹤數": "實時獲取",
                            "平均按讚": "熱門",
                            "互動率": "分析中",
                            "領域": f"搜尋結果: {tag}",
                            "認證狀態": "✅" if user.get("is_verified") else "🔗",
                            "個人網址": f"https://www.instagram.com/{user.get('username')}/"
                        })
            else:
                api_error = f"API 錯誤: {resp.status_code}"
        except Exception as e:
            api_error = f"連線異常: {str(e)}"

    # 備援機制：如果 API 沒抓到，顯示高品質本地庫
    if not results:
        from api_backup import INFLUENCER_DB, get_smart_category
        cat = get_smart_category(keyword)
        results = INFLUENCER_DB.get(cat, [{"帳號": "請搜尋特定關鍵字 (如: 美食)", "追蹤數": "-", "平均按讚": "-", "互動率": "-", "領域": "未匹配", "認證狀態": "❌", "個人網址": "#"}])

    return results, not api_connected, api_error

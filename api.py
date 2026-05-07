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
        except:
            pass
    return key

# --- 2024-2025 台灣網紅高品質資料庫 ---
INFLUENCER_DB = {
    "food": [
        {"帳號": "taipeieats", "追蹤數": "6.4萬 (估)", "平均按讚": 2100, "互動率": "3.3%", "領域": "台北美食/雙語", "認證狀態": "✅", "個人網址": "https://www.instagram.com/taipeieats/"},
        {"帳號": "foodie.taiwan", "追蹤數": "8.9萬 (估)", "平均按讚": 3500, "互動率": "4.1%", "領域": "全台美食/外送", "認證狀態": "❌", "個人網址": "https://www.instagram.com/foodie.taiwan/"},
        {"帳號": "martinispig", "追蹤數": "8.5萬 (估)", "平均按讚": 5600, "互動率": "6.8%", "領域": "吃貨豪豪/大胃王", "認證狀態": "❌", "個人網址": "https://www.instagram.com/martinispig/"},
        {"帳號": "yilan_yeh", "追蹤數": "4.7萬 (估)", "平均按讚": 4200, "互動率": "9.2%", "領域": "葉怡蘭/飲食作家", "認證狀態": "✅", "個人網址": "https://www.instagram.com/yilan_yeh/"},
        {"帳號": "selftaughtgourmet", "追蹤數": "5.8萬 (估)", "平均按讚": 2400, "互動率": "4.3%", "領域": "自學美食家/Fine Dining", "認證狀態": "❌", "個人網址": "https://www.instagram.com/selftaughtgourmet/"},
        {"帳號": "amberleeee35", "追蹤數": "5.0萬 (估)", "平均按讚": 3100, "互動率": "6.4%", "領域": "AMBER/質感餐廳", "認證狀態": "❌", "個人網址": "https://www.instagram.com/amberleeee35/"},
        {"帳號": "chichi_food___", "追蹤數": "1.8萬 (估)", "平均按讚": 850, "互動率": "4.9%", "領域": "奇奇美食/南部小吃", "認證狀態": "❌", "個人網址": "https://www.instagram.com/chichi_food___/"},
        {"帳號": "47_food.life", "追蹤數": "9.8萬 (估)", "平均按讚": 3200, "互動率": "3.3%", "領域": "專業食記/台北台中", "認證狀態": "❌", "個人網址": "https://www.instagram.com/47_food.life/"}
    ],
    "fitness": [
        {"帳號": "mimisparklemi", "追蹤數": "7.5萬 (估)", "平均按讚": 2800, "互動率": "3.7%", "領域": "咪咪/居家健身", "認證狀態": "✅", "個人網址": "https://www.instagram.com/mimisparklemi/"},
        {"帳號": "noviyang_", "追蹤數": "6.2萬 (估)", "平均按讚": 3100, "互動率": "5.0%", "領域": "楊諾威/健身教練", "認證狀態": "❌", "個人網址": "https://www.instagram.com/noviyang_/"},
        {"帳號": "lyna334998", "追蹤數": "5.5萬 (估)", "平均按讚": 2400, "互動率": "4.4%", "領域": "莉奈/健身攝影", "認證狀態": "❌", "個人網址": "https://www.instagram.com/lyna334998/"},
        {"帳號": "eric_fitness_tw", "追蹤數": "4.2萬 (估)", "平均按讚": 1800, "互動率": "4.3%", "領域": "Eric/科學訓練", "認證狀態": "❌", "個人網址": "https://www.instagram.com/eric_fitness_tw/"},
        {"帳號": "edward_0106", "追蹤數": "3.1萬 (估)", "平均按讚": 1200, "互動率": "3.9%", "領域": "張芋圓/陽光生活", "認證狀態": "❌", "個人網址": "https://www.instagram.com/edward_0106/"}
    ],
    "travel": [
        {"帳號": "ball_family_", "追蹤數": "9.4萬 (估)", "平均按讚": 4500, "互動率": "4.8%", "領域": "小球家庭/親子幽默", "認證狀態": "❌", "個人網址": "https://www.instagram.com/ball_family_/"},
        {"帳號": "vv_levia", "追蹤數": "9.5萬 (估)", "平均按讚": 5200, "互動率": "5.5%", "領域": "里唯/質感生活", "認證狀態": "✅", "個人網址": "https://www.instagram.com/vv_levia/"},
        {"帳號": "honique_mili", "追蹤數": "8.2萬 (估)", "平均按讚": 3800, "互動率": "4.6%", "領域": "米粒/溫馨家庭", "認證狀態": "❌", "個人網址": "https://www.instagram.com/honique_mili/"},
        {"帳號": "albeemami0921", "追蹤數": "5.5萬 (估)", "平均按讚": 2100, "互動率": "3.8%", "領域": "三寶媽/露營專家", "認證狀態": "❌", "個人網址": "https://www.instagram.com/albeemami0921/"},
        {"帳號": "alina_lifestyle", "追蹤數": "1.5萬 (估)", "平均按讚": 750, "互動率": "5.0%", "領域": "Alina/親子旅行", "認證狀態": "❌", "個人網址": "https://www.instagram.com/alina_lifestyle/"}
    ]
}

def get_smart_category(keyword):
    kw = keyword.lower()
    mapping = {
        "food": ["美食", "吃", "餐", "甜點", "咖啡", "下午茶", "小吃", "烘焙", "酒", "cafe", "restaurant"],
        "fitness": ["健身", "運動", "重訓", "體態", "減脂", "教練", "瑜珈", "跑步", "gym", "fitness", "workout"],
        "travel": ["旅遊", "旅行", "親子", "育兒", "飯店", "露營", "景點", "出國", "玩", "travel", "family"]
    }
    for cat, aliases in mapping.items():
        if any(alias in kw for alias in aliases):
            return cat
    return None

def search_instagram_influencers(keyword, follower_range):
    results = []
    api_connected = False
    api_error = "None"
    
    rapid_key = get_api_config()
    category = get_smart_category(keyword)
    
    # 1. 本地資料庫
    if category and category in INFLUENCER_DB:
        for inf in INFLUENCER_DB[category]:
            raw_count = inf["追蹤數"].replace("萬 (估)", "")
            try:
                num_count = float(raw_count) * 10000
                if follower_range[0] <= num_count <= follower_range[1]:
                    results.append(inf)
            except:
                results.append(inf)

    # 2. 最終修正：instagram191 正確搜尋路徑
    if rapid_key and "your_api_key" not in rapid_key:
        try:
            host = "instagram191.p.rapidapi.com"
            tag = keyword.replace("#", "").split()[0]
            
            # 嘗試 instagram191 的標籤媒體路徑
            url = "https://instagram191.p.rapidapi.com/v1/hashtag/info/"
            headers = {"x-rapidapi-key": rapid_key, "x-rapidapi-host": host}
            params = {"hashtag_name": tag}
            
            resp = requests.get(url, headers=headers, params=params, timeout=15)
            
            # 如果 404，嘗試替代路徑 /v1/search/
            if resp.status_code == 404:
                url = "https://instagram191.p.rapidapi.com/v1/search/hashtag/"
                params = {"query": tag}
                resp = requests.get(url, headers=headers, params=params, timeout=15)

            if resp.status_code == 200:
                api_connected = True
                data = resp.json()
                
                # 兼容不同的回傳結構
                items = data.get("items", []) or data.get("data", {}).get("items", [])
                
                if not items and "media_count" in data: # 如果是 info 接口，回傳可能是單一標籤資訊
                    results.append({
                        "帳號": f"#{tag} 趨勢中心",
                        "追蹤數": f"{data.get('media_count', 0)} 則貼文",
                        "平均按讚": "熱門中",
                        "互動率": "極高",
                        "領域": "Instagram 實時數據",
                        "認證狀態": "✅",
                        "個人網址": f"https://www.instagram.com/explore/tags/{tag}/"
                    })
                else:
                    for item in items[:8]:
                        user = item.get("user", {})
                        if user:
                            results.append({
                                "帳號": user.get("username", "未知"),
                                "追蹤數": "實時動態", 
                                "平均按讚": item.get("like_count", "點擊查看"),
                                "互動率": "實時解析",
                                "領域": f"#{tag} 實時趨勢",
                                "認證狀態": "✅" if user.get("is_verified") else "🔗",
                                "個人網址": f"https://www.instagram.com/{user.get('username')}/"
                            })
            else:
                api_error = f"API 錯誤: {resp.status_code} (內容: {resp.text[:50]})"
        except Exception as e:
            api_error = f"連線異常: {str(e)}"

    is_mock = not api_connected
    if not results:
        results = [{"帳號": "no_results", "追蹤數": "0", "平均按讚": 0, "互動率": "0%", "領域": "無匹配", "認證狀態": "❌", "個人網址": "https://www.instagram.com/"}]

    return results, is_mock, api_error

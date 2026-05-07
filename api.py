import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

# --- 台灣網紅 & KOC 精選資料庫 (V3.2 擴充 3C & 攝影分類) ---
INFLUENCER_DB = {
    "food": [
        {"帳號": "47_food.life", "追蹤數": 152000, "追蹤數_顯示": "15.2萬", "平均按讚": "4,200", "互動率": "3.5%", "領域": "美食日記/台北台中", "認證狀態": "✅", "個人網址": "https://www.instagram.com/47_food.life/"},
        {"帳號": "popyummy_mag", "追蹤數": 521000, "追蹤數_顯示": "52.1萬", "平均按讚": "12,000", "互動率": "2.1%", "領域": "波波發胖/流行媒體", "認證狀態": "✅", "個人網址": "https://www.instagram.com/popyummy_mag/"},
        {"帳號": "taipeieats", "追蹤數": 64000, "追蹤數_顯示": "6.4萬", "平均按讚": "2,100", "互動率": "3.3%", "領域": "台北美食/雙語", "認證狀態": "✅", "個人網址": "https://www.instagram.com/taipeieats/"},
        {"帳號": "chichi_food___", "追蹤數": 18500, "追蹤數_顯示": "1.8萬", "平均按讚": "850", "互動率": "4.9%", "領域": "奇奇美食/南部小吃", "認證狀態": "❌", "個人網址": "https://www.instagram.com/chichi_food___/"}
    ],
    "fitness": [
        {"帳號": "ashlee_xiu", "追蹤數": 182000, "追蹤數_顯示": "18.2萬", "平均按讚": "6,500", "互動率": "5.2%", "領域": "Ashlee/增肌減脂", "認證狀態": "✅", "個人網址": "https://www.instagram.com/ashlee_xiu/"},
        {"帳號": "peeta.gege", "追蹤數": 224000, "追蹤數_顯示": "22.4萬", "平均按讚": "7,800", "互動率": "3.1%", "領域": "Peeta葛格/科學健身", "認證狀態": "✅", "個人網址": "https://www.instagram.com/peeta.gege/"},
        {"帳號": "mimisparklemi", "追蹤數": 75000, "追蹤數_顯示": "7.5萬", "平均按讚": "2,800", "互動率": "3.7%", "領域": "咪咪/居家健身", "認證狀態": "✅", "個人網址": "https://www.instagram.com/mimisparklemi/"}
    ],
    "travel": [
        {"帳號": "keke_traveltheworld", "追蹤數": 321000, "追蹤數_顯示": "32.1萬", "平均按讚": "11,000", "互動率": "2.8%", "領域": "KEKE旅遊/打卡景點", "認證狀態": "✅", "個人網址": "https://www.instagram.com/keke_traveltheworld/"},
        {"帳號": "vv_levia", "追蹤數": 95000, "追蹤數_顯示": "9.5萬", "平均按讚": "5,200", "互動率": "5.5%", "領域": "里唯/質感生活", "認證狀態": "✅", "個人網址": "https://www.instagram.com/vv_levia/"},
        {"帳號": "alina_lifestyle", "追蹤數": 15000, "追蹤數_顯示": "1.5萬", "平均按讚": "750", "互動率": "5.0%", "領域": "Alina/親子旅行", "認證狀態": "❌", "個人網址": "https://www.instagram.com/alina_lifestyle/"}
    ],
    "tech": [
        {"帳號": "aottergirls", "追蹤數": 184000, "追蹤數_顯示": "18.4萬", "平均按讚": "5,500", "互動率": "3.0%", "領域": "電獺少女/科技生活", "認證狀態": "✅", "個人網址": "https://www.instagram.com/aottergirls/"},
        {"帳號": "ahui_3c", "追蹤數": 42000, "追蹤數_顯示": "4.2萬", "平均按讚": "1,200", "互動率": "2.8%", "領域": "廖阿輝/3C評論", "認證狀態": "✅", "個人網址": "https://www.instagram.com/ahui_3c/"},
        {"帳號": "apple_fan_3c", "追蹤數": 35000, "追蹤數_顯示": "3.5萬", "平均按讚": "950", "互動率": "2.7%", "領域": "蘋果迷/Apple產品", "認證狀態": "❌", "個人網址": "https://www.instagram.com/apple_fan_3c/"},
        {"帳號": "raymond.taiwan", "追蹤數": 21000, "追蹤數_顯示": "2.1萬", "平均按讚": "1,100", "互動率": "5.2%", "領域": "Raymond/攝影器材", "認證狀態": "❌", "個人網址": "https://www.instagram.com/raymond.taiwan/"}
    ]
}

def get_smart_category(keyword):
    kw = keyword.lower()
    mapping = {
        "food": ["美食", "吃", "餐", "甜點", "咖啡", "台北", "餐廳"],
        "fitness": ["健身", "運動", "重訓", "體態", "教練", "瑜珈"],
        "travel": ["旅遊", "旅行", "親子", "飯店", "景點", "出國"],
        "tech": ["3c", "手機", "電腦", "開箱", "科技", "評測", "相機", "apple", "科技", "開箱"]
    }
    for cat, aliases in mapping.items():
        if any(alias in kw for alias in aliases): return cat
    return None

def search_instagram_influencers(keyword, follower_range):
    results = []
    category = get_smart_category(keyword)
    min_f, max_f = follower_range
    
    if category and category in INFLUENCER_DB:
        for inf in INFLUENCER_DB[category]:
            if min_f <= inf['追蹤數'] <= max_f:
                results.append(inf)
    
    if not results:
        results = [{"帳號": "🔍 建議調整條件", "追蹤數": 0, "追蹤數_顯示": "-", "平均按讚": "-", "互動率": "-", "領域": f"未找到 '{keyword}' 的匹配", "認證狀態": "❌", "個人網址": "#"}]

    return results, False, "資料庫已同步：3C & 科技分類已加入"

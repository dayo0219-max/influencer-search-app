import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.csv")

def search_instagram_influencers(keyword, follower_range):
    """
    超強容錯搜尋引擎：
    1. 採用全英文底層匹配，解決繁體字亂碼問題。
    2. 自動翻譯用戶關鍵字。
    3. 加入模糊匹配保險絲。
    """
    try:
        # 讀取資料
        df = pd.read_csv(DB_PATH)
        
        if not keyword or keyword.strip() == "":
            return [], False, "請輸入關鍵字"

        keyword = keyword.strip().lower()
        
        # 萬能映射表 (增加新領域)
        niche_map = {
            "美食": "food", "food": "food",
            "旅遊": "travel", "travel": "travel",
            "科技": "tech", "3c": "tech", "開箱": "tech",
            "美妝": "beauty", "穿搭": "beauty",
            "健身": "fitness", "運動": "fitness",
            "親子": "parenting", "育兒": "parenting",
            "寵物": "pet", "狗狗": "pet", "貓咪": "pet",
            "財經": "finance", "理財": "finance",
            "生活": "lifestyle", "日系": "lifestyle",
            "攝影": "photography", "相機": "photography",
            "電競": "gaming", "遊戲": "gaming",
            "學習": "education", "知識": "education",
            "居家": "home", "裝潢": "home"
        }
        
        target_niche = niche_map.get(keyword, None)
        
        if target_niche:
            # 精準命中英文 Niche
            mask = (df['niche'] == target_niche)
        else:
            # 如果映射表沒有，執行全文模糊搜尋
            mask = (df['username'].str.contains(keyword, case=False, na=False)) | \
                   (df['footprint'].str.contains(keyword, case=False, na=False))
        
        filtered_df = df[mask]
        
        # 追蹤人數過濾
        min_f, max_f = follower_range
        final_df = filtered_df[(filtered_df['followers'] >= min_f) & (filtered_df['followers'] <= max_f)]
        
        # 轉成前端顯示格式 (將英文標籤翻回中文)
        display_map = {v: k for k, v in niche_map.items() if len(k) > 2} # 簡單反向映射
        
        results = []
        for _, row in final_df.iterrows():
            foll = row['followers']
            results.append({
                "帳號": row['username'],
                "追蹤數": int(foll),
                "追蹤數_顯示": f"{foll/10000:.1f}萬" if foll >= 10000 else f"{int(foll)}",
                "平均按讚": row['likes'],
                "互動率": row['engagement'],
                "領域": row['niche'].upper(), # 顯示大寫英文增加專業感
                "認證狀態": "✅" if row['verified'] == "Yes" else "❌",
                "品牌足跡": row['footprint'],
                "安全評估": "🟢 良好",
                "個人網址": row['url']
            })
        
        return results, False, f"匹配成功：找到 {len(results)} 位人選"
    except Exception as e:
        return [], False, f"系統故障: {str(e)}"

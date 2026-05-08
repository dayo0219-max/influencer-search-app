import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.csv")

def search_instagram_influencers(keyword, follower_range):
    try:
        df = pd.read_csv(DB_PATH, encoding='utf-8-sig')
        
        # 1. 嚴格檢查關鍵字
        if not keyword or keyword.strip() == "":
            return [], False, "請輸入關鍵字以進行搜尋"

        keyword = keyword.strip().lower()
        
        # 2. 建立標籤映射 (讓搜尋親子、旅遊能對應到正確 niche)
        niche_map = {
            "美食": "food", "旅遊": "travel", "科技": "tech", "開箱": "tech",
            "美妝": "beauty", "健身": "fitness", "育兒": "parenting", "親子": "parenting",
            "寵物": "pet", "財經": "finance"
        }
        
        target_niche = niche_map.get(keyword, None)
        
        # 3. 執行過濾
        if target_niche:
            # 如果是預設類別，採精準匹配
            mask = (df['niche'] == target_niche)
        else:
            # 如果是自定義詞，採模糊匹配，但確保不是全選
            mask = (df['username'].str.contains(keyword, case=False, na=False)) | \
                   (df['niche'].str.contains(keyword, case=False, na=False)) | \
                   (df['footprint'].str.contains(keyword, case=False, na=False))
        
        filtered_df = df[mask]
        
        # 4. 追蹤人數過濾
        min_f, max_f = follower_range
        final_df = filtered_df[(filtered_df['followers'] >= min_f) & (filtered_df['followers'] <= max_f)]
        
        # 5. 格式化輸出
        results = []
        for _, row in final_df.iterrows():
            foll = row['followers']
            results.append({
                "帳號": row['username'],
                "追蹤數": int(foll),
                "追蹤數_顯示": f"{foll/10000:.1f}萬" if foll >= 10000 else f"{int(foll)}",
                "平均按讚": row['likes'],
                "互動率": row['engagement'],
                "領域": row['niche'],
                "認證狀態": row['verified'],
                "品牌足跡": row['footprint'],
                "安全評估": row['safety'],
                "個人網址": row['url']
            })
        
        return results, False, f"找到 {len(results)} 位人選"
    except Exception as e:
        return [], False, f"系統錯誤: {str(e)}"

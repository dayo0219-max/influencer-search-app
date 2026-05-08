import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.csv")

def search_instagram_influencers(keyword, follower_range):
    """
    穩健版：使用英文欄位名稱，避免亂碼衝突，支援模糊搜尋
    """
    try:
        # 強制指定編碼讀取
        df = pd.read_csv(DB_PATH, encoding='utf-8-sig')
        
        # 英文標籤映射表
        cat_map = {
            "美食": "food", "food": "food",
            "旅遊": "travel", "travel": "travel",
            "健身": "fitness", "fitness": "fitness",
            "3c": "tech", "科技": "tech", "tech": "tech",
            "美妝": "beauty", "beauty": "beauty",
            "育兒": "parenting", "親子": "parenting",
            "寵物": "pet", "pet": "pet",
            "財經": "finance", "理財": "finance"
        }
        
        target_niche = cat_map.get(keyword.lower(), None)
        
        # 模糊搜尋邏輯：帳號、領域、足跡任一匹配即可
        if target_niche:
            mask = (df['niche'] == target_niche)
        else:
            # 全文模糊匹配
            mask = (df['username'].str.contains(keyword, case=False, na=False)) | \
                   (df['niche'].str.contains(keyword, case=False, na=False)) | \
                   (df['footprint'].str.contains(keyword, case=False, na=False))
        
        filtered_df = df[mask]
        
        # 追蹤人數過濾
        min_f, max_f = follower_range
        final_df = filtered_df[(filtered_df['followers'] >= min_f) & (filtered_df['followers'] <= max_f)]
        
        # 格式化輸出
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
        return [], False, f"搜尋系統異常: {str(e)}"

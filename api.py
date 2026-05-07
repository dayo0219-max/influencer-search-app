import pandas as pd
import os

# 取得目前檔案路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.csv")

def get_smart_category(keyword):
    kw = keyword.lower()
    mapping = {
        "food": ["美食", "吃", "餐", "甜點", "咖啡", "台北", "餐廳", "koc", "小網紅"],
        "fitness": ["健身", "運動", "重訓", "體態", "教練", "瑜珈", "koc"],
        "travel": ["旅遊", "旅行", "親子", "飯店", "景點", "出國", "koc"],
        "tech": ["3c", "手機", "電腦", "開箱", "科技", "評測", "相機", "apple"],
        "beauty": ["美妝", "穿搭", "保養", "時尚", "化妝", "beauty"]
    }
    for cat, aliases in mapping.items():
        if any(alias in kw for alias in aliases): return cat
    return None

def search_instagram_influencers(keyword, follower_range):
    """
    大數據版：從 CSV 讀取並過濾上千筆資料
    """
    try:
        # 讀取資料庫
        df = pd.read_csv(DB_PATH)
        
        # 轉換數值型態確保過濾正確
        df['追蹤數'] = pd.to_numeric(df['追蹤數'], errors='coerce')
        
        # 關鍵字過濾
        category = get_smart_category(keyword)
        if category:
            mask = (df['領域'] == category)
        else:
            mask = df['帳號'].str.contains(keyword, case=False, na=False) | \
                   df['領域'].str.contains(keyword, case=False, na=False)
        
        filtered_df = df[mask]
        
        # 人數區間過濾
        min_f, max_f = follower_range
        final_df = filtered_df[(filtered_df['追蹤數'] >= min_f) & (filtered_df['追蹤數'] <= max_f)]
        
        # 轉換回列表格式供介面顯示
        results = final_df.to_dict('records')
        
        # 格式化顯示用的數字 (例如 152000 -> 15.2萬)
        for res in results:
            count = res['追蹤數']
            if count >= 10000:
                res['追蹤數_顯示'] = f"{count/10000:.1f}萬"
            else:
                res['追蹤數_顯示'] = f"{count:,}"
        
        return results, False, f"已從資料庫載入 {len(results)} 筆結果"
    except Exception as e:
        return [], False, f"資料庫讀取失敗: {str(e)}"

import pandas as pd

def read_file(file_path):
    """
    讀取 Excel 或 CSV 檔案，並返回 DataFrame。
    :param file_path: 檔案路徑
    :return: pandas DataFrame
    """
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, encoding='utf-8')
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(file_path, engine='openpyxl')
        else:
            raise ValueError("不支援的檔案格式，請使用 CSV 或 Excel 檔案！")
        
        print(df.head())  # 顯示前五筆資料
        return df
    except Exception as e:
        print(f"讀取檔案時發生錯誤: {e}")

# 測試讀取檔案
file_path = "sample\Car Sales.xlsx"  # xlsx csv
df = read_file(file_path)
def read_html(html_path):
    # 開啟並讀取 HTML 檔案
    with open(html_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    
    return html_content

if __name__ == "__main__":
    html_path = "sample/sample_html.html"
    extracted_text = read_html(html_path)
    print(extracted_text)  # 輸出 HTML 內容

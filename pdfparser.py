import os
import cv2
import pytesseract
from pypdf import PdfReader
from pdf2image import convert_from_path
import fitz

poppler_path = r"C:\Users\david01.tseng\Documents\projects\parsers\poppler-24.08.0\Library\bin"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def read_pdf(pdf_path):
    """
    讀取 PDF 內的純文字（pypdf）and OCR 擷取圖片內的文字（pytesseract）
    :param pdf_path: PDF 檔案路徑
    :return: PDF 內的所有文字（含 OCR 轉換的內容）
    """
    text = ""  

    # 讀取 PDF 內嵌純文字
    # try:
    #     pdf_reader = PdfReader(pdf_path)
    #     for page in pdf_reader.pages:
    #         text += page.extract_text() + "\n"
    # except Exception as e:
    #     print(f"讀取 PDF 純文字時發生錯誤: {e}")

    # 將 PDF 轉換為圖片（用於 OCR）
    try:
        images = convert_from_path(pdf_path, poppler_path=poppler_path)  # 轉換 PDF 為圖片

        for i, image in enumerate(images):
            if not os.path.exists("extracted_img"):
                os.makedirs("extracted_img")
            # 儲存臨時圖片（可選，不存也行）
            temp_img_path = f"extracted_img/pdf_page_{i+1}.png"
            image.save(temp_img_path, "PNG")

            # 讀取圖片進行 OCR
            img_cv = cv2.imread(temp_img_path)
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)  # 轉為灰階提升 OCR 準確度

            # 使用 Tesseract 進行 OCR
            ocr_text = pytesseract.image_to_string(gray, lang="eng+chi_tra")  # 支援中英文
            text += f"--- Page {i+1} ---\n{ocr_text}\n\n"

    #         # 移除臨時圖片（如果有存檔）
    #         # os.remove(temp_img_path)

    except Exception as e:
        print(f"OCR 解析圖片時發生錯誤: {e}")

    return text

# 從 PDF 擷取所有圖片並存入指定資料夾
def extract_images_from_pdf(pdf_path, output_folder):
    """
    從 PDF 擷取所有圖片並存入指定資料夾
    :param pdf_path: PDF 檔案路徑
    :param output_folder: 輸出圖片的資料夾
    """
    try:
        os.makedirs(output_folder, exist_ok=True)  # 確保輸出資料夾存在
        doc = fitz.open(pdf_path)
        image_count = 0  # 記錄圖片數量

        for page_num, page in enumerate(doc):
            images = page.get_images(full=True)
     
            for img_index, img in enumerate(images):
                    xref = img[0]  # 取得圖片的 xref ID
                    base_image = doc.extract_image(xref)  # 擷取圖片
                    image_bytes = base_image["image"]
                    img_ext = base_image["ext"]  # 取得圖片副檔名 (如 png, jpeg)
                    
                    img_filename = f"page_{page_num+1}_img_{img_index+1}.{img_ext}"
                    img_filepath = os.path.join(output_folder, img_filename)

                    with open(img_filepath, "wb") as img_file:
                        img_file.write(image_bytes)

                    image_count += 1
                    print(f"已儲存圖片: {img_filepath}")

        print(f"總共擷取 {image_count} 張圖片，儲存於 {output_folder}")

    except Exception as e:
        print(f"擷取圖片時發生錯誤: {e}")

if __name__ == "__main__":
    pdf_file = "sample\deepseek-r1.pdf"  # 替換為你的 PDF 檔案
    extracted_text = read_pdf(pdf_file)
    # extract_images_from_pdf(pdf_file, "extracted_img")
    print(extracted_text)
    with open("extracted_txt/pdf_output_OCR.txt", "w", encoding="utf-8") as txt_file:
            txt_file.write(extracted_text)

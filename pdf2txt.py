import fitz
from paddleocr import PaddleOCR

def extract_text_from_pdf(pdf_path):
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    result = ocr.ocr(pdf_path, cls=True)
    text = ""
    for i in range(len(result)):
        if result[i]:
            for j in range(len(result[i])):
                text += result[i][j][-1][0]
    return text


# PDF文件路径
pdf_path = '/root/data/pdf/StartingStrengthBasic.pdf'  # 例如：'example.pdf'

# 提取文字
extracted_text = extract_text_from_pdf(pdf_path)

# 将提取的文字保存到TXT文件
with open('/root/data/pdf/StartingStrengthBasic.txt', 'w', encoding='utf-8') as f:
    f.write(extracted_text)

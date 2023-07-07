from flask import Flask, render_template, request
from PIL import Image
import os
import pytesseract

app = Flask(__name__)

# Tesseract OCR 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'C:/Users/advan/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'

# 이미지에서 텍스트 추출하는 함수
def ocr_image(image):
    text = pytesseract.image_to_string(image)
    return text

# 웹 페이지 렌더링
@app.route('/')
def home():
    return render_template('index.html')

# 이미지 업로드 및 OCR 수행
@app.route('/upload', methods=['POST'])
def upload():
    # 업로드된 이미지 가져오기
    image = request.files['image']
    
    # PIL Image 객체로 변환
    pil_image = Image.open(image)
    
    # OCR 수행
    extracted_text = ocr_image(pil_image)
    
    # 추출된 텍스트와 이미지 파일 경로를 웹 페이지에 전달
    return render_template('result.html', text=extracted_text)
if __name__ == '__main__':
    app.run()

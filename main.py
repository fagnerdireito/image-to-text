#opencv
import pytesseract, re
import cv2
from pytesseract import Output
import requests
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)

@app.route('/')
def homepage():
    return 'A simple web app to read images and return the text'

@app.route('/readimage', methods=['POST'])
def ler_imagem():
    input_json = request.get_json(force=True) 
    url = input_json['url']
    r = requests.get(url)
    # pegar a hora atual
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    # transformar em timestamp
    filename = str(timestamp) + '.jpg'
    # salvar a imagem
    with open("images/"+filename, 'wb') as f:
        f.write(r.content)
    # ==========
    # ler imagem
    img = cv2.imread(r'images/'+filename)
    # converter para escala de cinza
    gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # apontar para o diretorio do tesseract
    pytesseract.pytesseract.tesseract_cmd = 'D:\\www\\Tesseract-OCR\\tesseract.exe'
    # resultado do texto
    result = pytesseract.image_to_string(gry)

    conta=0
    for item in result.split("\n"):
        conta += 1
        # print(f"{conta}" + " - " + item)
        if conta == 12:
            numero_comprovante = item
    
    return jsonify({"filename": filename, "numero_comprovante": numero_comprovante})
    
    

app.run(debug=True)
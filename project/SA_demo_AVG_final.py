# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 20:12:27 2020

@author: artem
"""
from sentiment_classifier import LogRegTfidfClf
from flask import Flask, render_template, request
from codecs import open
import time
import warnings
warnings.filterwarnings('ignore')


app = Flask(__name__)


print("Preparing classifier")
start_time = time.time()
classifier = LogRegTfidfClf()
print("Classifier is ready")
print(time.time() - start_time, "seconds")
check_message = classifier.get_prediction_message('Проверка')
print(check_message)

@app.route("/", methods=["POST", "GET"])
def index_page(text="", prediction_message=""):
    if request.method == "POST":
        logfile = open("demoAVG_logs.txt", "a", "utf-8")
        text = request.form["text"]
        
        if text.replace(' ','').replace("\n",'').replace("\r",'') =='':
            prediction_message='Введите отзыв!'
            
        else:        
            print(text)
            logfile.write("<response>\n")
            logfile.write(text+"\n")
            prediction_message = classifier.get_prediction_message(text)
            print(prediction_message)
            logfile.write(prediction_message+"\n")
            logfile.write("</response>\n")
            logfile.close()
            
    return render_template('Form.html', text=text, prediction_message=prediction_message) #вывод результатов


@app.route("/model", methods=["POST", "GET"])
def model_page():            
    try:
        return render_template('description.html', model=classifier.model,message=check_message)
    except:
        return render_template('description.html', message=check_message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

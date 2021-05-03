# -*- coding: utf-8 -*-
"""
Created by Shyam Chanduri
MIT License
"""


import webbrowser
from threading import Timer
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

# @app.route('/upload', methods = ['POST', 'GET'])
# def upload():
#     if request.method == 'POST':
#         #file = request.form['file_photo']
#         # with open(file, 'r') as f:
#         #user = file
#         user = "aaa"
#         return redirect(url_for("user", usr=user))
#     else:
#         return render_template("home.html")
    

# @app.route("/<usr>")
# def user(usr):
#     return f"<h1>{usr}</h1>"

def open_browser():
      webbrowser.open_new('http://127.0.0.1:2000/')

if __name__ == "__main__":
      Timer(1, open_browser).start();
      app.run(port=2000)
      
      
import os, os.path, random, hashlib, sys, json
from flask import Flask, flash, render_template, redirect, request, url_for, jsonify, session, Response

app = Flask(__name__)
app.secret_key = '9je0jaj09jk9dkakdwjnjq'

@app.route('/')
def main():
        return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/handle_data', methods=['POST'])
def handle_data():
    i=0
    print(request.form['start'])
    while(1):
        try:
            print(request.form['location'+str(i)])
            i+=1
        except:
            break
    return render_template('index.html')

app.run(host='0.0.0.0', port=80)
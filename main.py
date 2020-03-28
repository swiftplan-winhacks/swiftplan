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
    try:
        print(request.form['name'])
        print(request.form['day'])
        print(request.form['type'])
        print(request.form['localization'])
        print(request.form['hour'])
        print(request.form['minute'])
        print(request.form['duration'])
    except:
        pass
    return render_template('index.html')

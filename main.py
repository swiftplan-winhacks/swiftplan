import os, os.path, random, hashlib, sys, json
from flask import Flask, flash, render_template, redirect, request, url_for, jsonify, session, Response
from database import *

app = Flask(__name__)
app.secret_key = '9je0jaj09jk9dkakdwjnjq'
db = Database("swiftplan")

@app.route('/')
def main():
        return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/addUser', methods=['POST'])
def addUser():
    if(request.method == "POST"):
        #robimy uz plain texrem czemu nie
        db.addUser(request.form['username'], request.form['password'])
    else:
        print("didn't add the user")
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    if(request.method == "POST"):
        #robimy uz plain texrem czemu nie
        db.addUser(request.form['username'], request.form['password'])
    else:
        print("didn't log in")
    return render_template('index.html')

@app.route('/handle_data', methods=['POST'])
def handle_data():
    try:
        t = Timeframe("01.01.1234", "13:00","02.01.1234", "13:21", "3:00")
        e = Event(f"a{i}", "nothing", "lol", Location(00.123,00.123), True, t)
        name = request.form['name']
        day = request.form['day']
        prrequest.form['type'])
        print(request.form['localization'])
        print(request.form['hour'])
        print(request.form['minute'])
        print(request.form['duration'])
        
    except:
        pass
    return render_template('index.html')

app.run('0.0.0.0', 80)
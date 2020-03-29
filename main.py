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
    # if('username' not in session):
    #    return redirect(url_for('login'))
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
        #również prymitywne. To MVP to można
        session['username'] = request.form['username']
    else:
        print("didn't log in")
    return render_template('index.html')

@app.route('/addevent', methods=['POST'])
def addEvent():
        return render_template('addevent.html')

@app.route('/handle_data', methods=['POST'])
def handle_data():
    fixed = 0
    try:
        a = request.form('fixed')
        fixed = 1
    except:
        fixed = 0

    name = request.form['name']
    day = request.form['day']
    day = day.replace("/", ".")
    print(fixed)
    print(day)
    print(request.form['type'])
    print(request.form['location'])
    print(request.form['duration'])
    print(request.form['day'])
    print(request.form['hour'])
    print(request.form['minute'])
    print(request.form['end_day'])
    print(request.form['end_hour'])
    print(request.form['end_minute'])
    return render_template('index.html')

app.run('0.0.0.0', 80)

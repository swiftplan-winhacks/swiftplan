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
    if('username' not in session):
        redirect(url_for('login'))
    else:
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
    print(request.form['name'])
    print(request.form['day'])
    print(request.form['type'])
    print(request.form['location'])
    print(request.form['duration'])
    print(request.form['fixed'])
    return render_template('index.html')

app.run('0.0.0.0', 80)

import os, os.path, random, hashlib, sys, json
from flask import Flask, flash, render_template, redirect, request, url_for, jsonify, session, Response
from database import *
from datetime import date
from planner import Planner

app = Flask(__name__)
app.secret_key = '9je0jaj09jk9dkakdwjnjq'
db = Database("swiftplan")



@app.route('/')
def main():
    session['username'] = "test" #do usuniecia jak zrobisz login
    db.addUser("test", "test")
    return redirect(url_for('index'))

@app.route('/index')
def index():
    # if('username' not in session):
    #    return redirect(url_for('login'))
    return render_template('index.html', events=db.fetchEvents(session['username']))


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

@app.route('/addevent', methods=['POST', 'GET'])
def addEvent():
    return render_template('addevent.html')

@app.route('/handle_data', methods=['POST'])
def handle_data():
    name = request.form['name']
    type = request.form['type']
    desc = request.form['description']
    day = request.form['day']
    day = day.replace("/", ".")
    
    hours = request.form['hour']
    if(len(hours) < 2):
        hours = '0' + hours
    minutes = request.form['minute']
    if(len(minutes) < 2):
        minutes = '0' + minutes
    time = f"{hours}:{minutes}"

    lat = request.form['lat']
    lng = request.form['long']
    duration = f"00:{request.form['duration']}"
    fixed = None
    try:
        #Fixed
        a = request.form('fixed')
        fixed = 1

    except:
        #Not fixed
        fixed = 0

    if(fixed):
        l = Location(lat, lng)
        t = Timeframe(
            start_date = day,
            start_time = time,
            end_date = day,
            end_time = time,
            duration = duration
            )
        e = Event(name, type, desc, l, fixed, t)
    else:
        l = Location(lat, lng)
        today = str(date.today()).split("-")
        today = f"{today[2]}.{today[1]}.{today[0]}"
        print(today)
        t = Timeframe(
            start_date = today,
            start_time = "08:00",
            end_date = day,
            end_time = time,
            duration = duration
            )
        e = Event(name, type, desc, l, fixed, t)

    db.addEvent(session['username'], e)

    HOME_LOCATION = Location(52.22977, 21.01178)  # PKIN
    all_events = db.fetchEvents(session['username'])
    planner = Planner(all_events, HOME_LOCATION)
    planner.plan()

    for event in all_events:
        db.updateEvent(session['username'], event)

    print("success")
    return render_template('index.html')

app.run('0.0.0.0', 80)

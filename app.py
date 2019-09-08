from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from apscheduler.scheduler import Scheduler
import random, json, config, atexit

app = Flask(__name__)
app.secret_key=b'supersecret1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locations.db'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0#avoids caching
db = SQLAlchemy(app)

cron = Scheduler(daemon=True)#create cron job thread for periodic deletion
cron.start()

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html',uniquePath=assignUniquePath())

#generates a unique path, and inserts it into the db. returns the path
def assignUniquePath():#get path
    uniquePath = 0
    unique = False #is the current path unique?
    while not unique: #make sure the url is UNIQUE
        unique = True
        uniquePath = random.randint(10000, 99999)
        result = db.engine.execute(text("select path from locat where path = {}"
                .format(uniquePath)))
        for _ in result: #if no matches, continue will not be ran 
            unique = False
    sql='''INSERT INTO locat (path,long,lat,time) 
        VALUES ({},0,0, CURRENT_TIMESTAMP )'''.format(uniquePath) #insert the new path
    db.engine.execute(text(sql))
    return uniquePath

@app.route('/updateLocat',methods=['POST'])
def updateLocat():#gets locatiopn data from js ajax and updates db, updates in a set interval
    print("update")
    sql='''UPDATE locat 
        SET long = {}, lat = {}
        where path = {}'''.format(
        request.form['long'],request.form['lat'],
        request.form['path'])#update new coords
    db.engine.execute(text(sql))
    return "Done"

@app.route('/<path:uniquePath>',methods=['GET'])
def map(uniquePath):#map code
  
    sql='''select long,lat from locat where
    path = {}
    '''.format(uniquePath)
    results = db.engine.execute(text(sql))
    for coord in results:
        return render_template('map.html',uniquePath=uniquePath,
                                        long = coord[0],lat = coord[1],
                                        key = config.MAP_KEY) 
    return render_template('map.html',uniquePath=-1) 

@cron.interval_schedule(hours=1)
def cronDeleter():#cron process for deleting at 1 hour interval
    sql=''' DELETE FROM locat WHERE
    time < DATETIME('NOW', '-2 hours') '''#delete all rows created > 2 hours ago
    db.engine.execute(text(sql))

# close cron job when web app is stopped
atexit.register(lambda: cron.shutdown(wait=False))

if __name__ =="__main__":
    #SQLALCHEMY_TRACK_MODIFICATIONS = False
    app.run(host="localhost",port=5000,debug=True)


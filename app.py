from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import random, json, config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locations.db'#connect db
db = SQLAlchemy(app)#initiate db

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

@app.route('/updateCoord',methods=['POST'])
def updateCoord(uniquePath):
    sql='''select long,lat from locat where
    path = {}
    '''.format(uniquePath)
    results = db.engine.execute(text(sql))
    for coord in results:
        return  jsonify( {'long' : coord[0], 'lat' : coord[1]} )                           
    return -1


if __name__ =="__main__":
    app.run(host="localhost",port=5000,debug=True)


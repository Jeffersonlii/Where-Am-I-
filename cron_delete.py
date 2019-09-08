from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import random, json, config

app = Flask(__name__)
app.secret_key=b'supersecret1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locations.db'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0#avoids caching
db = SQLAlchemy(app)

sql=''' DELETE FROM locat WHERE
time < DATETIME('NOW', '-2 hours') '''#delete all rows created > 2 hours ago
db.engine.execute(text(sql))
    

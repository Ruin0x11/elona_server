# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, Response
from contextlib import closing
from datetime import datetime

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

DATABASE = '/tmp/elona.db'

def connect_to_database():
    return sqlite3.connect(DATABASE)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        for i in range(0,50):
            db.execute('insert into chat (time, kind, name, descr, text, addr) values (?, ?, ?, ?, ?, ?)',
                     [datetime.now().strftime("%s"), 1, "弱気ものprin", "は猫に殺された", "なむ", "127.0.0.1"])
        db.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def type(x):
    return {
        0: 'chat',
        1: 'dead',
        2: 'wish',
    }.get(x, 0)

@app.route("/text.txt")
def text():
    response = app.send_static_file('text.txt')
    return response


@app.route("/log.txt")
def vote():
    response = ""
    first = query_db('select * from chat order by id desc limit 1', one=True)
    no = first['id']+1 if first else 1
    response += str(no) + "<C>\n<!--START-->\n"
    for line in query_db('select * from chat order by id desc limit 30'):
        date = datetime.fromtimestamp(line['time']).strftime("%m/%d(%I)")
        response += str(line['id']) + '%' + date + '%' + type(line['kind']) + line['name'] + line['descr'] + '「' + line['text'] + '」%' + line['addr'] + '%\n'
    response += "<!--END-->\n<!-- WebTalk v1.6 --><center><small><a href='http://www.kent-web.com/' target='_top'>WebTalk</a></small></center>"
    return Response(response, mimetype='text/plain')
    

if __name__ == "__main__":
    app.run()

# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, Response
from contextlib import closing
from datetime import datetime
import codecs

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
        date = int(datetime.now().strftime("%s"))
        for i in range(0,200):
            db.execute('insert into chat (time, kind, name, descr, text, addr) values (?, ?, ?, ?, ?, ?)',
                     [int(date), 1, "弱気ものprin", "は猫に殺された", "なむ", "127.0.0.1"])
            db.execute('insert into vote (name, votes, addr, time, totalvotes, rank) values (?, ?, ?, ?, ?, ?)',
                     ["弱気ものprin" + str(i), 10, '127.0.0.1', date, 1000, i])
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
    response = "<!--START-->\n%\n素敵な異名コンテスト♪1  [１ヶ月で自動リセット]%\nYour favorite alias♪1  [Auto reset every month]%"
    return Response(response, mimetype='text/plain')


@app.route("/log.txt")
def log():
    response = ""
    first = query_db('select * from chat order by id desc limit 1', one=True)
    no = first['id']+1 if first else 1
    response += str(no) + "<C>\n<!--START-->\n"
    for line in query_db('select * from chat order by id desc limit 30'):
        date = datetime.fromtimestamp(line['time']).strftime("%m/%d(%I)")
        response += str(line['id']) + '%' + date + '%' + type(line['kind']) + line['name'] + line['descr'] + '「' + line['text'] + '」%' + line['addr'] + '%\n'
    response += "<!--END-->\n<!-- WebTalk v1.6 --><center><small><a href='http://www.kent-web.com/' target='_top'>WebTalk</a></small></center>"
    return Response(response, mimetype='text/plain')
    

@app.route("/vote.txt")
def vote():
    response = ""
    first = query_db('select * from chat order by id desc limit 1', one=True)
    i = 1
    no = first['id']+1 if first else 1
    response += str(no) + "<C>\n<!--START-->\n"
    for line in query_db('select * from vote limit 100'):
        date = datetime.fromtimestamp(line['time']).strftime("%s")
        response += str(i) + '<>' + line['name'] + '<>' + str(line['votes']) + '<>' + line['addr'] + '<>' + date + '#' + str(line['totalvotes']) + '#' + str(line['rank']) + '#<>\n'
        i += 1
    response += "<!--END-->\n<!-- WebTalk v1.6 --><center><small><a href='http://www.kent-web.com/' target='_top'>WebTalk</a></small></center>"
    return Response(response, mimetype='text/plain')


@app.route("/cgi-bin/vote/votec.cgi")
def add_vote():
    no = request.args.get('no')
    mode = request.args.get('mode')
    vote = codecs.decode(request.args.get('vote'), 'unicode_escape')
    votestr = str.encode(vote, "raw_unicode_escape").decode("shift-jis")
    return "dood"

if __name__ == "__main__":
    app.run()

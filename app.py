from imp import init_builtin
from mimetypes import init
from flask import Flask, render_template,redirect, request,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sb.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    
    def __init__(self,name,score):
        self.name = name
        self.score = score

    def __repr__(self):
        return '<Player %r>' % self.name

@app.route('/')
def sendMainPage():
    return redirect(url_for('index'))

@app.route("/index.html", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        score = request.form.get("score")
        if not username:
            pass
        elif not score:
            pass
        
        plr = Player(username,score)
        db.session.add(plr)
        db.session.commit()

    return render_template('index.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/table.html')
def table():
    players = Player.query.all()
    dic = dict()
    for i in range(len(players)):
        elem = {players[i].name:players[i].score}
        dic.update(elem)
    dic = {k: v for k, v in sorted(dic.items(), reverse=True, key = lambda item:item[1])}    
    return render_template('table.html',values=dic)       


from flask import Flask, redirect, url_for, request, jsonify, render_template
from bson import ObjectId

app = Flask(__name__)

SECRET_KEY = 'SPARTA'

import jwt

app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.gok1afs.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

# 페이지 영역
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('first.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/first')
def first():
    return render_template('first.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/button')
def button():
    return render_template('button.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/loding')
def loding():
    return render_template('loding.html')

@app.route('/product')
def product():
    return render_template('product.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
from flask import Flask, redirect, url_for, request, jsonify, render_template
from bson import ObjectId



SECRET_KEY = 'SPARTA'

import jwt

import hashlib

import datetime

app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://mookim:2406@cluster0.sptev7m.mongodb.net/Cluster0?retryWrites=true&w=majority')

db = client.dbsparta_plus_week4

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







#################################
##  로그인을 위한 API            ##
#################################
# 중복체크기능
@app.route('/api/dup', methods=['POST'])
def api_dub():

    id_receive = request.form['id_give']
    result = db.user.find_one({'id': id_receive})

    if result is not None:
        return jsonify({'result': 'fail', 'msg': '이미 사용되고 있는 아이디입니다'})

    else:
        return jsonify({'result': 'success'})


# [회원가입 API]
# id, pw, nickname을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/api/register', methods=['POST'])
def api_register():

    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    # nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    result = db.user.find_one({'id': id_receive})

    if result is not None:
        return jsonify({'result': 'fail', 'msg': 'ID 중복 여부를 확인해 주세요'})

    else:
        db.user.insert_one({'id': id_receive, 'pw': pw_hash})
        return jsonify({'result': 'success'})


# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')


        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
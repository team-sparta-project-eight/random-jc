from flask import Flask, redirect, url_for, request, jsonify, render_template

SECRET_KEY = 'SPARTA'

import jwt

import hashlib

import datetime

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.gok1afs.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


# 페이지 영역
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    if token_receive is None:
        return render_template('first.html')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('login.html', user_info=user_info)

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
        return jsonify({'result': 'success', 'msg': '사용가능한 아이디입니다'})


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


# 권한 부여 코드
@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')
    # try / catch 문?
    # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.
    if token_receive is not None:
        return render_template('button.html')
    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        user_info = db.user.find_one({'userid': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success'})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


@app.route("/product", methods=["GET"])
def product_get():
    product_list = list(db.product.find({}, {'_id': False}))

    return jsonify({'product': product_list})


@app.route("/commentget", methods=["GET"])
def comment_get():
    comment_list = list(db.comment_list.find({}, {'_id': False}))

    return jsonify({'comment': comment_list})


# 댓글 데이터 저장
@app.route("/Postcomment", methods=["POST"])
def save_comment():
    comment_receive = request.form['comment_give']
    name_pk_receive = request.form['name_pk_give']

    comment_list = list(db.comment_list.find({}, {'_id': False}))
    count = len(comment_list) + 1

    doc = {
        'comment': comment_receive,
        'num': count,
        'name_pk': name_pk_receive,
    }
    db.comment_list.insert_one(doc)

    return jsonify({'msg': '댓글 작성 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

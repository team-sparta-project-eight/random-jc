
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)


from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.vkxpfdw.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('test4.html')

@app.route("/product", methods=["GET"]) ##통합을하면 script에 있는 Math.random 이 있는 곳 부터 인식을 못합니다.
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

    doc={
        'comment': comment_receive,
        'num' : count,
        'name_pk': name_pk_receive,
    }
    db.comment_list.insert_one(doc)

    return jsonify({'msg': '댓글 작성 완료!'})
    # 삭제와 수정을 주석처리한 이유는 토큰값을 받는다는 전제하에 코드를 작성하였는데 애초에 이어지지가 않아서 다른 부분이라도 보여드릴려고 주석처리 하였습니다.
#댓글 삭제    ##
#@app.route('/detail_delete', methods=["POST"])
#def del_comment():
#    token_receive = request.cookies.get('mytoken')  #쿠키에서 토큰 값 받아오기
#    num_receive = request.form['num_give'] #num값 받아오기
#    names = db.comment.find_one({'num': int(num_receive)}, {'_id': False})

#    try:
#        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#        name = db.users.find_one({'username': payload['id']},{'_id':False}) #회원디비생성후 대조
#        print(name)
#        if names['name'] == name['profile_name']: #이것도 디비 회원정보가 어떻게 담기는지 확인 후 db설정 // 토큰내부에 유저 네임과 db 유저컬렉션안에 데이터 네임이 동일하면 이뤄짐.
#            db.comment.delete_one({'num':int(num_receive)}) #선택한 댓글의 num값과 Db안에 같은 num값을 가진 댓글 삭제
#            return jsonify({'msg': '삭제완료!'})
#        else:
#            return jsonify({'msg': '다른사람이 작성한 글입니다. 삭제할 수 없습니다.'})
#    except jwt.ExpiredSignatureError:
#        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
#    except jwt.exceptions.DecodeError:
#        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

#댓글 수정
#@app.route('/detail_upload', methods=["POST"])
#def del_comment():
#    token_receive = request.cookies.get('mytoken')  #쿠키에서 토큰 값 받아오기
#    num_receive = request.form['num_give'] #num값 받아오기
#    comment_receive = request.form['comment_give'] 수정값 받아오기
#    names = db.comment.find_one({'num': int(num_receive)}, {'_id': False})

#    try:
#        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#        name = db.users.find_one({'username': payload['id']},{'_id':False}) #회원디비생성후 대조
#        print(name)
#        if names['name'] == name['profile_name']: #이것도 디비 회원정보가 어떻게 담기는지 확인 후 db설정 // 토큰내부에 유저 네임과 db 유저컬렉션안에 데이터 네임이 동일하면 이뤄짐.
#            db.comment.update_one({'num':int(num_receive),{'$set':{'comment':comment_receive}}) #선택한 댓글의 num값과 Db안에 같은 num값을 가진 댓글 수정
#            return jsonify({'msg': '수정완료!'})
#        else:
#            return jsonify({'msg': '다른사람이 작성한 글입니다. 수정할 수 없습니다.'})
#    except jwt.ExpiredSignatureError:
#        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
#    except jwt.exceptions.DecodeError:
#        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)



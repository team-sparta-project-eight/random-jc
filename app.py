
from flask import Flask, render_template, request, jsonify , session
app = Flask(__name__)


from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.vkxpfdw.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/product", methods=["GET"])
def product_get():
    product_list = list(db.product.find({}, {'_id': False}))

    return jsonify({'product': product_list})

# 댓글 데이터 저장
@app.route('/Comment', methods=["post"])
def Comment():
    postwrite_pk_receive = request.form['product_pk_give']
    comments_receive = request.form['comments_give']


    comment_count = db.Counts.find_one({'count_pk': 0}, {'_id': False})
    count = comment_count['comment_count'] + 1

    doc = {
        'product_pk': int(postwrite_pk_receive),
        'comments_pk': count,
        'comments': comments_receive,
        'comments_flag': 0,
        # 접속유저 pk(세션)
        'comments_id': db.User.find_one({'user_pk': 5}, {'_id': False}),

    }
    db.Comment.insert_one(doc)
    db.Counts.update_one({'count_pk': 0}, {'$set': {'comment_count': count}})

    return jsonify({'msg': '댓글 작성 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)



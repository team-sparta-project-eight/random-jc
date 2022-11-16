
from flask import Flask, render_template, request, jsonify
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
@app.route("/product", methods=["POST"])
def comment():
    comment_receive = request.form['comment_give']
    name_pk_receive = request.form['name_pk_give']
    doc={
        'commment': comment_receive,
        'name_pk': name_pk_receive
    }
    db.product.update_one({'name': name_pk_receive  }, {'$set': {'comment': comment_receive}})


    return jsonify({'msg': '댓글 작성 완료!'})




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)



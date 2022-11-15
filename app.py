from flask import Flask, render_template, request, jsonify , session
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.vkxpfdw.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/https://starbugs.herokuapp.com/api/menus", methods=["POST"])
def web_result_page_post():
    id_receive = request.form['id_give']
    name_receive = request.form['name_give']
    image_receive = request.form['image_give']
    doc = {
        'id' : id_receive,
        'name' : name_receive,
        'image' : image_receive
    }
    db.product.insert_one(doc)
    return jsonify({'msg': '주문 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)



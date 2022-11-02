from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:<sparta>@cluster0.ycdwiqy.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbmini

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/likes", methods=["POST"])
def likes_post():

    likes_count = list(db.likes.find({}, {'_id': False}))
    count = len(likes_count) + 1

    doc = {
        'num': int(count),
    }

    db.likes.insert_one(doc)

    return jsonify({'msg':'좋아요!'})

# 좋아요 수 보여주기
@app.route("/likes", methods=["GET"])
def likes_get():

    likes_count = list(db.likes.find({},{'_id':False}))
    return jsonify({'likes': likes_count})

@app.route("/comments", methods=["POST"])
def comment_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    doc = {'name': name_receive,
           'comment': comment_receive}
    db.comments_visit.insert_one(doc)

    return jsonify({'msg':'방명록 작성 완료!'})

@app.route("/comments", methods=["GET"])
def comment_get():
    comment_list = list(db.comments_visit.find({}, {'_id': False}))
    return jsonify({'comments': comment_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
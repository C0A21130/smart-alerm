from flask import Flask,request,jsonify,render_template
import json
import pymongo
import datetime

app = Flask(__name__)
db_url = "mongodb+srv://test:testpass@cluster0.091dd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
file = "./data/data.json"
week = ["sun","mon","tue","wed","thu","fri","sat"]

# dbへ接続
def get_db(user):
    client = pymongo.MongoClient(db_url)
    db = client.myFirstDatabase
    col = db[user]
    return col

# webからアクセス
@app.route("/")
def index():
    return render_template("index.html")

# testページ
@app.route("/test")
def set_timer():
    return "<h1>Hello Flask</h1>"

# 設定した起きる時間を取得
@app.route("/get_timer",methods=["GET"])
def get_timer():
    user = request.args.get("user")
    col = get_db(user)
    d = col.find_one()
    return jsonify(d["timer"])

# 設定した起きる時間を変更
@app.route("/put_timer", methods=["PUT"])
def put_timer():
    j = request.get_json()
    user = j["user"]
    timer = j["timer"]
    col = get_db(user)
    result = col.update_one({"user": user},{"$set":{"timer":timer}})
    return jsonify({"user":user,"timer":timer})

# 今までの睡眠時間を確認
@app.route("/get_sleep_time", methods=["GET"])
def get_sleep_time():
    user = request.args.get("user")
    col = get_db(user)
    d = col.find_one()
    return jsonify(d["sleep_times"])

# 今までの睡眠時間を記録
@app.route("/post_sleep_time",methods=["POST"])
def post_sleep_time():
    j = request.get_json()
    user = j["user"]
    time = int(j["time"])
    dt = datetime.datetime.now()
    today = f"{dt.year}/{dt.month}/{dt.day}"

    col = get_db(user)
    d = col.find_one()
     
    if (today in d["sleep_times"]):
        t = d["sleep_times"][today]
        time+=t
    d["sleep_times"][today] = time
    result = col.update_one({"user":user},{"$set":{"sleep_times":d["sleep_times"]}})
    return jsonify(d["sleep_times"])

# 新しいアカウントを作成
@app.route("/post_account", methods=["POST"])
def post_account():
    j = request.get_json()
    user = j["user"]
    timer = j["timer"]
    mail = j["mail"]
    new_user = {
        "user": user,
        "address": mail,
        "timer": timer,
        "sleep_times":{}
    }
    col = get_db(user)
    col.insert_one(new_user)
    return jsonify(new_user)

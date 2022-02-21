from flask import Flask,request,jsonify
import json
import datetime

app = Flask(__name__)
file = "./data/data.json"
week = ["sun","mon","tue","wed","thu","fri","sat"]

# テストページ
@app.route("/")
def index():
    return "<h1>HELLO Flask</h1>"

# 設定した起きる時間を取得
@app.route("/get_timer",methods=["GET"])
def get_timer():
    user = request.args.get("user")
    with open(file,mode="r") as f:
        d = json.load(f)
    return jsonify(d[user]["timer"])

# 設定した起きる時間を変更
@app.route("/put_timer", methods=["PUT"])
def put_timer():
    j = request.get_json()
    user = j["user"]
    timer = j["timer"]
    with open(file,mode="r") as f:
        d = json.load(f)
    d[user]["timer"]= timer
    with open(file,mode="w") as f:
        json.dump(d,f,indent=2)
    return jsonify({"name":user,"timer":timer})

# 今までの睡眠時間を確認
@app.route("/get_sleep_time", methods=["GET"])
def get_sleep_time():
    user = request.args.get("user")
    with open(file,mode="r") as f:
        d = json.load(f)
    return jsonify(d[user]["sleep_times"])

# 今までの睡眠時間を記録
@app.route("/post_sleep_time",methods=["POST"])
def post_sleep_time():
    j = request.get_json()
    time = int(j["timer"])
    user = j["user"]
    dt = datetime.datetime.now()
    today = f"{dt.year}/{dt.month}/{dt.day}"

    with open(file,mode="r") as f:
        d = json.load(f)
    if (today in d[user]["sleep_times"]):
        t = d[user]["sleep_times"][today]
        timer+=t
    d[user]["sleep_times"][today] = timer
    with open(file,mode="w") as f:
        json.dump(d,f,indent=2)
    return jsonify({"user": user, "time":timer})

# 新しいアカウントを作成
@app.route("/post_account", methods=["POST"])
def post_account():
    j = request.get_json()
    user = j["user"]
    time = j["timer"]
    mail = j["mail"]
    timer = dict(zip(week, timer))
    new = {
    user:
    {
        "address": mail,
        "timer": timer,
        "sleep_times":{"day": 000}
    }
    }

    with open(file,mode="r") as f:
        d = json.load(f)
    d.update(new)
    with open(file,mode="w") as f:
        json.dump(d,f,indent=2)
    return user

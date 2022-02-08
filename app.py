from flask import Flask,request,jsonify
import json
import datetime

app = Flask(__name__)
file = "./data/data.json"

# テストページ
@app.route("/")
def index():
    return "<h1>HELLO Flask</h1>"

# 設定した起きる時間を取得
@app.route("/timer",methods=["GET"])
def get_timer():
    name = request.args.get("user")
    with open(file,mode="r") as f:
        d = json.load(f)
    return jsonify(d[name]["timer"])

# 寝た時間を記録
@app.route("/sleep_time",methods=["POST"])
def post_sleep_time():
    j = request.get_json()
    time = j["time"]
    user = j["user"]
    dt = datetime.datetime.now()
    today = f"{dt.year}/{dt.month}/{dt.day}"

    with open(file,mode="r") as f:
        d = json.load(f)
    d[user]["sleep_times"][today] = time
    with open(file,mode="w") as f:
        json.dump(d,f,indent=2)
    return jsonify({"user": user, "time":time})

# 新しいアカウントを作成
@app.route("/post_account", methods=["POST"])
def post_account():
    j = request.get_json()
    user = j["user"]
    time = j["time"]
    mail = j["mail"]
    week = ["sun","mon", "tue", "wen", "thu", "fry", "sat"]
    timer = dict(zip(week, time))
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
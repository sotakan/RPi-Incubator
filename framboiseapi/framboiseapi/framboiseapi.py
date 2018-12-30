from flask import Flask , request , jsonify
from flask_restful import Api, Resource, reqparse
import mysql.connector
import uuid
import json

app = Flask(__name__)

class db:
    database = mysql.connector.connect(host = "192.168.1.101" , user = "framboise_api" , passwd = "" , database = "framboise")
    cursor = database.cursor()

@app.route("/register" , methods = ["GET"])
def register_incubator():
    auth = request.headers.get("auth_code")
    if len(auth) != 4 or auth != int:
        return jsonify({"error" : "Bad auth_code"}) , 400
    uuid = str(uuid.uuid1())
    sql = "INSERT INTO `new_auths` (`uuid`, `auth_code`, `done`) VALUES (`%s`, `%s`, `0`)" % uuid, auth_code
    db.cursor.execute(sql)
    db.database.commit()
    return jsonify({"result" : "OK" , "uuid" : uuid}) , 201

@app.route("/register/check" , methods = ["GET"])
def check_register():
    uuid = request.headers.get("auth_code")
    sql = "SELECT * FROM `new_auths` WHERE `auth_code` = `%s`" % auth_code
    db.cursor.execute(sql)
    result = db.cursor.fetchall()
    if result[2] == 0:
        return jsonify({"registered" : False}) , 200
    elif result[2] == 1:
        sql =
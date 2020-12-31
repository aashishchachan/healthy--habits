import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app=Flask(__name__)
    client= MongoClient("mongodb+srv://aashishchachan:cH19sH@cluster0.fstu1.mongodb.net/test?authSource=admin&replicaSet=atlas-ikrm4f-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")
    app.db=client.user_data

    @app.route('/')
    def index():
        return render_template("health.html")

    @app.route('/signup')
    def signup():
        return render_template("signup.html")    

    @app.route('/register', methods=["GET", "POST"])
    def register():
        register_username=request.form.get("register_username")
        register_password=request.form.get("register_password")
        register_name=request.form.get("register_name")

        app.db.login_credentials.insert({"info":[register_username, register_password, register_name]})

        return "thanks for registering!"

    @app.route('/account', methods=["POST"])
    def data():
        dat= [e for e in app.db.login_credentials.find({})] #list of dictionaries
        username = request.form.get("login_username")
        password = request.form.get("login_password")

        for ind in range(len(dat)):
            temp = dat[ind]["info"]
            if temp[0]==username and temp[1]==password:
                    return render_template("welcome.html", name=temp[2])
        return "Incorrect username or password"    

    return app
from flask import Flask, render_template
import os
import json 
import datetime

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])

def index():
    return render_template("index.html")

@app.route("/article", methods=["GET","POST"])

def article():
    return render_template("article.html")

@app.route("/admin", methods=["GET","POST"])

def admin():
    return render_template("admin.html")

@app.route("/edit", methods=["GET","POST"])

def edit():
    return render_template("edit.html")

@app.route("/new", methods=["GET","POST"])

def new():
    return render_template("new.html")

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, make_response
from functools import wraps
import os
import json 

app = Flask(__name__)

JSONFILE = "articles.json"

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == "admin" and auth.password == "password":
            return f(*args, **kwargs)
        
        return make_response("Could not verify your login.", 401, {"WWW-Authenticate": "Basic realm='Login Required'"})
    
    return decorated

@app.route("/", methods=["GET","POST"])

def index():
    return render_template("index.html")

@app.route("/article", methods=["GET","POST"])

def article():
    return render_template("article.html")

# Admin pages

@app.route("/admin", methods=["GET","POST"])
@auth_required

def admin():
    return render_template("admin.html")

@app.route("/edit", methods=["GET","POST"])
@auth_required

def edit():
    return render_template("edit.html")

@app.route("/new", methods=["GET","POST"])
@auth_required

def new():
    with open(JSONFILE, "r") as file:
        data = json.load(file)

    try:
        if request.method == "POST":
            title = request.form["title"]
            date = request.form["date"]
            content = request.form["content"]

            if not title or not date or not content:
                print("Form field empty")
                return render_template("new.html", title = None)

            iD = 1
            current_ids = []

            for item in data:
                current_ids.append(item["id"])

            while iD in current_ids:
                iD += 1

            data.append({
                    "id": iD,
                    "title": title,
                    "date": date,
                    "content": content
                })
            
            with open(JSONFILE, "w") as file:
                json.dump(data,file,indent=4)

            return render_template("new.html", title = title, date = date)
        
    except ValueError:
        print("Form field empty")
        return render_template("new.html",title = None)
    
    return render_template("new.html",title = None)

if __name__ == "__main__":

    if not os.path.exists(JSONFILE):
        with open(JSONFILE, "w") as file:
            json.dump([],file)

    app.run(debug=True)
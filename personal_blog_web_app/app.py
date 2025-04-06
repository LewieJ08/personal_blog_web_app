from flask import Flask, render_template, request, make_response, redirect, url_for
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

def format_content(content,max_chars):
    lines = []
    for paragraph in content.splitlines():  
        words = paragraph.split()
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 > max_chars:
                lines.append(current_line.rstrip())
                current_line = ""

            current_line += word + " "

        if current_line:
            lines.append(current_line.rstrip())

    return '\r\n'.join(lines)

@app.route("/", methods=["GET","POST"])

def index():
    with open(JSONFILE, "r") as file:
        data = json.load(file)

    return render_template("index.html", articles = data)

@app.route("/article/<int:article_id>", methods=["GET","POST"])

def article(article_id):
    with open(JSONFILE, "r") as file:
        data = json.load(file)

    for item in data:
        if item["id"] == article_id:
            article = item

    return render_template("article.html", article = article)

# Admin pages

@app.route("/admin", methods=["GET","POST"])
@auth_required

def admin():
    with open(JSONFILE, "r") as file:
        data = json.load(file)

    new_articles = []

    if request.method == "POST":
        delete = request.form["delete"]

        delete = delete.split(" ",1)
        article_id = delete[1]

        for item in data:
            if item["id"] != int(article_id):
                new_articles.append(item)

        if len(new_articles) == len(data):
            print("Article not found.")
            return render_template("admin.html", articles = data)
        
        with open(JSONFILE, "w") as file:
            json.dump(new_articles,file,indent=4)

        return redirect(url_for('admin'))

    return render_template("admin.html", articles = data)
 

@app.route("/edit/<int:article_id>", methods=["GET","POST"])
@auth_required

def edit(article_id):
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
            
            content = format_content(content, 30)

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
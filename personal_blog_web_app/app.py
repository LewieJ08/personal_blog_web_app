from flask import Flask, render_template, request
import os
import json 

app = Flask(__name__)

JSONFILE = "articles.json"

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
    with open(JSONFILE, "r") as file:
        data = json.load(file)

    try:
        if request.method == "POST":
            title = request.form["title"]
            date = request.form["date"]
            content = request.form["content"]

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
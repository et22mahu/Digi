from flask import Flask, render_template, request
import os
import sqlite3

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "myth_database.db")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("query", "")

@app.route("/contact")
def contact():
    return render_template("contact.html")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM `Mythical Creatures` WHERE `Mythical Creature Name` LIKE ?",
        (f"%{query}%",),
    )

    results = cursor.fetchall()
    conn.close()

    return render_template(
        "search_results.html",
        query=query,
        results=results
    )


if __name__ == "__main__":
    app.run(debug=True)



@app.route("/greek")
def greek():
    return render_template("greek.html")

@app.route("/norse")
def norse():
    return render_template("norse.html")

@app.route("/egyptian")
def egyptian():
    return render_template("egyptian.html")
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

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT
        mc.*,
        li.`Mythology source`
    FROM `Mythical Creatures` AS mc
    JOIN `Location Information` AS li
        ON mc.`Country ID` = li.`Country ID`
    WHERE mc.`Mythical Creature Name` LIKE ?
    """,
    (f"%{query}%",),
)

    results = cursor.fetchall()
    conn.close()

    return render_template(
        "search_results.html",
        query=query,
        results=results
    )

@app.route("/contact")
def contact():
    return render_template("contact.html")

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

@app.route("/mayan")
def mayan():
    return render_template("mayan.html")

@app.route("/japanese")
def japanese():
    return render_template("japanese.html")

@app.route("/roman")
def roman():
    return render_template("roman.html")

@app.route("/mesopotamian")
def mesopotamian():
    return render_template("mesopotamian.html")

@app.route("/celtic")
def celtic():
    return render_template("celtic.html")

@app.route("/hindu")
def hindu():
    return render_template("hindu.html")

@app.route("/aztec")
def aztec():
    return render_template("aztec.html")

@app.route("/chinese")
def chinese():
    return render_template("chinese.html")

@app.route("/native_american")
def native_american():
    return render_template("native_american.html")

@app.route("/maori")
def maori():
    return render_template("maori.html")

@app.route("/hawaiian")
def hawaiian():
    return render_template("hawaiian.html")
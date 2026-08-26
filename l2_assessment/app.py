from flask import Flask, render_template, request, session, redirect, url_for
import os
import sqlite3

app = Flask(__name__)

app.secret_key = "mythology-bodleian-secret-key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "myth_database.db")


FONT_CLASSES = {
    "Ancient Greek": "ancient-greek-font",
    "Ancient Egyptian": "ancient-egyptian-font",
    "Norse": "norse-font",
    "Japanese": "japanese-font",
    "Roman": "roman-font",
    "Mayan": "mayan-font",
    "Mesopotamian": "mesopotamian-font",
    "Celtic": "celtic-font",
    "Hindu": "hindu-font",
    "Aztec": "aztec-font",
    "Chinese": "chinese-font",
    "Native American": "native-american-font",
    "Maori": "maori-font",
    "Hawaiian": "hawaiian-font"
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/toggle_easy_read")
def toggle_easy_read():

    if session.get("easy_read", False):
        session["easy_read"] = False
    else:
        session["easy_read"] = True

    return redirect(request.referrer or url_for("home"))


@app.route("/search")
def search():
    query = request.args.get("query", "")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            mc.`Myth ID`,
            mc.`Mythical Creature Name`,
            mc.`Appearance`,
            mc.`Behaviour`,
            mc.`Danger Rating`,
            mc.`Intelligence`,
            mc.`Habitat`,
            mc.`Country ID`,
            mc.`Images`,
            li.`Mythology source`
        FROM `Mythical Creatures` AS mc
        JOIN `Location Information` AS li
            ON mc.`Country ID` = li.`Country ID`
        WHERE mc.`Mythical Creature Name` LIKE ?
        """,
        (f"%{query}%",),
    )

    results = cursor.fetchall()

    formatted_results = []

    for row in results:

        mythology = row[9]

        font_class = FONT_CLASSES.get(
            mythology,
            "creature-name"
        )

        formatted_results.append({
            "id": row[0],
            "name": row[1],
            "appearance": row[2],
            "behaviour": row[3],
            "danger": row[4],
            "intelligence": row[5],
            "habitat": row[6],
            "country_id": row[7],
            "image": row[8],
            "mythology": row[9],
            "font_class": font_class
        })

    conn.close()

    return render_template(
        "search_results.html",
        query=query,
        results=formatted_results
    )


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/submit_contact", methods=["POST"])
def submit_contact():

    name = request.form["name"]
    email = request.form["email"]
    feedback_type = request.form["type"]
    message = request.form["message"]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO Feedback (
            "Name",
            "Email",
            "Type",
            "Message"
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            name,
            email,
            feedback_type,
            message
        )
    )

    conn.commit()
    conn.close()

    return redirect(url_for("contact"))


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


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, session, redirect, url_for
import os
import sqlite3
from datetime import datetime

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

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            mc.`Mythical Creature Name`,
            mc.`Appearance`,
            mc.`Images`,
            li.`Mythology source`
        FROM `Mythical Creatures` AS mc
        JOIN `Location Information` AS li
            ON mc.`Country ID` = li.`Country ID`
        ORDER BY mc.`Myth ID`
        """
    )

    creatures = cursor.fetchall()

    conn.close()

    if creatures:

        week_number = datetime.now().isocalendar().week

        creature = creatures[
            (week_number - 1) % len(creatures)
        ]

        name = creature[0]
        appearance = creature[1]
        image = creature[2]
        mythology = creature[3]

        font_class = FONT_CLASSES.get(
            mythology,
            "creature-name"
        )

        creature_of_the_week = {
            "name": name,
            "appearance": appearance,
            "image": image,
            "mythology": mythology,
            "font_class": font_class
        }

    else:

        creature_of_the_week = None

    return render_template(
        "index.html",
        creature=creature_of_the_week
    )


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


MYTHOLOGY_ROUTES = {
    "greek": "Ancient Greek",
    "norse": "Norse",
    "egyptian": "Ancient Egyptian",
    "japanese": "Japanese",
    "roman": "Roman",
    "mayan": "Mayan",
    "mesopotamian": "Mesopotamian",
    "celtic": "Celtic",
    "hindu": "Hindu",
    "aztec": "Aztec",
    "chinese": "Chinese",
    "native_american": "Native American",
    "maori": "Maori",
    "hawaiian": "Hawaiian"
}


@app.route("/mythology/<mythology>")
def mythology_page(mythology):

    mythology_name = MYTHOLOGY_ROUTES.get(mythology)

    if mythology_name is None:
        return "Mythology not found", 404

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
        WHERE li.`Mythology source` = ?
        ORDER BY mc.`Mythical Creature Name`
        """,
        (mythology_name,)
    )

    results = cursor.fetchall()

    conn.close()

    formatted_results = []

    for row in results:

        font_class = FONT_CLASSES.get(
            mythology_name,
            "creature-name"
        )

        formatted_results.append({
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

    return render_template(
        "mythology.html",
        mythology=mythology_name,
        creatures=formatted_results
    )

@app.route("/greek")
def greek():
    return redirect(url_for("mythology_page", mythology="greek"))


@app.route("/norse")
def norse():
    return redirect(url_for("mythology_page", mythology="norse"))


@app.route("/egyptian")
def egyptian():
    return redirect(url_for("mythology_page", mythology="egyptian"))


@app.route("/japanese")
def japanese():
    return redirect(url_for("mythology_page", mythology="japanese"))


@app.route("/roman")
def roman():
    return redirect(url_for("mythology_page", mythology="roman"))


@app.route("/mayan")
def mayan():
    return redirect(url_for("mythology_page", mythology="mayan"))


@app.route("/mesopotamian")
def mesopotamian():
    return redirect(url_for("mythology_page", mythology="mesopotamian"))


@app.route("/celtic")
def celtic():
    return redirect(url_for("mythology_page", mythology="celtic"))


@app.route("/hindu")
def hindu():
    return redirect(url_for("mythology_page", mythology="hindu"))


@app.route("/aztec")
def aztec():
    return redirect(url_for("mythology_page", mythology="aztec"))


@app.route("/chinese")
def chinese():
    return redirect(url_for("mythology_page", mythology="chinese"))


@app.route("/native_american")
def native_american():
    return redirect(url_for("mythology_page", mythology="native_american"))


@app.route("/maori")
def maori():
    return redirect(url_for("mythology_page", mythology="maori"))


@app.route("/hawaiian")
def hawaiian():
    return redirect(url_for("mythology_page", mythology="hawaiian"))

if __name__ == "__main__":
    app.run(debug=True)
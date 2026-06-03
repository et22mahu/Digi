from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("query")

    conn = sqlite3.connect("myth_database.db")
    cursor = conn.cursor

    cursor.execute("""
        SELECT *
        FROM creatures
        WHERE [Mythical Creature Name] LIKE?
    """, (f"%{query}%",))

    results = cursor.fetchall()

    conn.close()

    return render_template(
        "search_results.html",
        query=query,
        results=results
    )


if __name__ == "__main__":
    app.run(debug=True)
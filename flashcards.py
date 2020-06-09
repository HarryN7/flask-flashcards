from flask import Flask, render_template, abort, jsonify, request, redirect, url_for

from model import db

app = Flask(__name__)

view_counter = 0

@app.route("/")
def welcome():
    return render_template(
        "welcome.html",
        header = "Hola Mundo",
        cards = db
    )

@app.route("/add_card", methods=["GET","POST"])
def add_card():
    if request.method == "POST":
        # form has been submitted, process data
        card = {"question": request.form['question'],
                "answer": request.form['answer']}
        db.append(card)
        return redirect(url_for('card_view', index=len(db) - 1))
    else:
        return render_template("add_card.html")

@app.route("/card/<int:index>", methods=["GET","POST"])
def card_view(index):
    if request.method == "POST":
        del db[index]
        index -= 1
    try:
        card = db[index]
        return render_template(
            "card.html",
            card=card,
            index=index,
            max_index = len(db) - 1
        )
    except IndexError:
        abort(404)

@app.route("/api/cards/")
def api_cards():
    return jsonify(db)

@app.route("/api/card/<int:index>")
def api_single_card(index):
    try:
        return db[index]
    except IndexError:
        abort(404)
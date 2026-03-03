from flask import Blueprint, jsonify, request, redirect
from db import WrongQuote, Quote, Author
import db
import random
import pickle
from peewee import fn

api = Blueprint("/api", __name__, url_prefix="/api")

with open("apikeys.pkl", "rb") as f:
    apikeys = pickle.load(f)


if False:
    import logging
    logger = logging.getLogger('peewee')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)


@api.route("/")
def docs():
    return redirect("https://codeberg.org/uonel/falsch-zugeordnete-zitate#api")


@api.route("/wrongquotes", methods=["GET", "POST"])
def api_wrongquotes():
    if request.method == "GET":
        wrongquotes = []

        no_text = ("no_text" in request.args) and (
            request.args.get("no_text") == "true"
        )

        selected = WrongQuote.select_all_foreign_keys_resolved()

        # Select Quotes from db
        if ("quote" in request.args) and ("author" in request.args):
            selected = selected.where(
                (WrongQuote.author.id == int(request.args.get("author")))
                & (WrongQuote.quote.id == int(request.args.get("quote")))
            )
        elif "quote" in request.args:
            selected = selected.where(
                WrongQuote.quote.id == int(request.args.get("quote"))
            )
        elif "author" in request.args:
            selected = selected.where(
                WrongQuote.author.id == int(request.args.get("author"))
            )

        if sort := request.args.get("sort"):
            desc = False
            if sort[0] == "-":
                sort = sort[1:]
                desc = True
            sortkeys = {
                "random": fn.Random(),
                "quote": WrongQuote.quote.quote.desc() if desc else WrongQuote.quote.quote,
                "author": WrongQuote.author.author.desc() if desc else WrongQuote.author.author,
                "score": WrongQuote.score.desc() if desc else WrongQuote.score,
            }
            if sort not in sortkeys:
                return "Supported orderings: " + ", ".join(list(sortkeys) + [f"-{key}" for key in sortkeys if key != "random"]), 400
            selected = selected.order_by(sortkeys[sort], WrongQuote.id)

        if count := request.args.get("count"):
            selected = selected.limit(int(count))

        for wrongquote in selected:
            if (
                (
                    (
                        request.args.get("search").lower()
                        in wrongquote.quote.quote  + " " + wrongquote.author.author
                    )
                    if "search" in request.args
                    else True
                )
                and (wrongquote.get_score() >= int(request.args.get("min_score")))
                if "min_score" in request.args
                else True
            ):
                wq_dict = wrongquote.get_dict()
                if no_text:
                    del wq_dict["author"]["author"]
                    del wq_dict["quote"]["quote"]
                    del wq_dict["quote"]["author"]["author"]
                wrongquotes.append(wq_dict)
        # Simulate existing quote
        if (
            ("simulate" in request.args)
            and ("author" in request.args)
            and ("quote" in request.args)
            and (request.args.get("simulate") == "true")
            and (len(wrongquotes) == 0)
        ):
            quote = Quote.get_or_none(Quote._pk == request.args.get("quote"))
            author =  Author.get_or_none(Author._pk == request.args.get("author"))
            if quote and author:
                wrongquotes.append(
                    {
                        "id": None,
                        "quote": quote.get_dict(),
                        "author": author.get_dict(),
                        "voted": 0,
                        "showed": 0,
                        "rating": 0,
                        "checked": True,
                    }
                )
        return jsonify(wrongquotes)

    elif request.method == "POST":
        wrongquote = WrongQuote.create(
            quote=Quote.get_by_id(int(request.form["quote"])),
            author=Author.get_by_id(int(request.form["author"])),
            contributed_by=request.form["contributed_by"],
        )
        return jsonify(wrongquote.get_dict())


@api.route("/wrongquotes/random", methods=["GET"])
def api_wrongquotes_random():
    min_rating = 0
    if "min_rating" in request.args:
        min_rating = request.args.get("min_rating", default=0, type=int)

    count = 1
    if "count" in request.args:
        count = int(request.args.get("count", default=1, type=int))

    selected = (
        WrongQuote.select_all_foreign_keys_resolved()
        .where(WrongQuote.rating >= min_rating)
        .order_by(fn.Random())
        .limit(count)
    )

    wrongquotes = [wq.get_dict() for wq in selected]

    return jsonify(wrongquotes)


@api.route("/wrongquotes/<int:pk>", methods=["GET", "POST"])
def api_wrongquotes_id(pk):
    try:
        if request.method == "GET":
            return jsonify(WrongQuote.get_by_id(pk).get_dict())
        elif request.method == "POST":
            if int(request.form["vote"]) in [-1, 1]:
                wrongquote = WrongQuote.get_by_id(pk)
                wrongquote.rating += int(request.form["vote"])
                wrongquote.save()
                return jsonify(wrongquote.get_dict())
    except db.WrongQuote.DoesNotExist:
        return jsonify({"error":"quote not found"}), 404

@api.route("/wrongquotes/count")
def api_wrongquotes_counts():
    return jsonify(len(WrongQuote.select()))


@api.route("/quotes", methods=["GET", "POST"])
def quotes():
    if request.method == "GET":
        quotes = []
        if "author" in request.args:
            select = Quote.select().where(Quote.author == request.args.get("author"))
        else:
            select = Quote.select()
        for quote in select:
            quotes.append(quote.get_dict())
        return jsonify(quotes)
    elif request.method == "POST":
        if "id" not in request.form:
            quote = Quote.create(
                quote=request.form["quote"],
                author=Author.get_by_id(int(request.form["author"])),
            )
            return jsonify(quote.get_dict())
        else:
            if request.form["key"] in apikeys:
                quote = Quote.get_by_id(int(request.form["id"]))
                quote.quote = request.form["quote"]
                quote.save()
                return jsonify(quote.get_dict())


@api.route("/quotes/<int:pk>")
def quote(pk):
    try:
        return jsonify(Quote.get_by_id(pk).get_dict())
    except db.Quote.DoesNotExist:
        return jsonify({"error":"quote not found"}), 404


@api.route("/quotes/count")
def quote_count():
    return jsonify(len(Quote.select()))


@api.route("/authors", methods=["GET", "POST"])
def authors():
    if request.method == "POST":
        if "id" not in request.form:
            author = Author.create(author=request.form["author"])
            return jsonify(author.get_dict())
        else:
            if request.form["key"] in apikeys:
                author = Author.get_by_id(request.form["id"])
                author.author = request.form["author"]
                author.save()
                return jsonify(author.get_dict())

    elif request.method == "GET":
        authors = []
        for author in Author.select():
            authors.append(author.get_dict())
        return jsonify(authors)


@api.route("/authors/<int:pk>")
def author(pk):
    try:
        return jsonify(Author.get_by_id(pk).get_dict())
    except db.Author.DoesNotExist:
        return jsonify({"error":"author not found"}), 404

@api.route("/authors/count")
def author_count():
    return jsonify(len(Author.select()))

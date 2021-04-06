import os
from random import choice, shuffle
from flask import Flask
from flask import session, flash, g, redirect, render_template, request, Response


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "voting.sqlite"),
    )
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from db import WrongQuote, Quote, Author
    from api import api

    app.register_blueprint(api)

    @app.route("/hello")
    def hello():
        return "Hello, World"

    @app.route("/", methods=("GET",))
    def start():
        g.page = "start"

        quotes = list(WrongQuote.select().where(WrongQuote.checked == True))
        quotes = sorted(quotes, key=lambda quote: quote.showed)
        final_quotes = []
        for quote in quotes:
            if quote.showed != quotes[-1].showed and not (
                ("votes" in session) and (quote._pk in session["votes"])
            ):
                final_quotes.append(quote)

        if len(final_quotes) == 1:
            final_quotes.append(choice(quotes))
            session["votes"] = []
        elif len(final_quotes) == 0:
            final_quotes = quotes
            session["votes"] = []

        shuffle(final_quotes)
        for quote in final_quotes[:100]:
            if quote.showed > 5 and quote.voted / quote.showed > 0.5:
                final_quotes.append(quote)
            elif quote.showed <= 5:
                final_quotes.append(quote)

            if quote.showed > 15 and quote.voted / quote.showed < 0.1:
                quote.delete_instance()
                final_quotes.remove(quote)

        zit1 = choice(final_quotes)
        zit2 = choice(final_quotes)
        while zit1 == zit2:
            zit1 = choice(final_quotes)
            zit2 = choice(final_quotes)

        g.zit1id = zit1._pk
        g.zit2id = zit2._pk
        g.zit1q = zit1.quote.quote
        g.zit1a = zit1.author.author
        g.zit2q = zit2.quote.quote
        g.zit2a = zit2.author.author
        return render_template("start.html")

    @app.route("/abstimmung", methods=("POST",))
    def abstimmung():
        if "zit" in request.form:
            voted, not_voted = request.form["zit"].split("-")
            voted_quote = WrongQuote.get_by_id(int(voted))
            voted_quote.voted += 1
            voted_quote.showed += 1
            voted_quote.save()
            not_voted_quote = WrongQuote.get_by_id(int(not_voted))
            not_voted_quote.showed += 1
            not_voted_quote.save()
            if "votes" not in session:
                session["votes"] = []
            session["votes"] += [int(voted), int(not_voted)]
        return redirect("/")

    @app.route("/einreichen", methods=("GET", "POST"))
    def einreichen():
        g.page = "einreichen"
        g.email = session["email"] if "email" in session else ""
        if request.method == "POST":
            quote = request.form["quote"].strip()
            new_author = request.form["wrongauthor"].strip()
            real_author = request.form["realauthor"].strip()
            contributed_by = request.form["email"]
            if real_author not in [a.author for a in Author.select()]:
                real_author_db = Author.create(
                    author=real_author, contributed_by=contributed_by
                )
            else:
                real_author_db = Author.get(Author.author == real_author)
            if quote not in [q.quote for q in Quote.select()]:
                quote_db = Quote.create(
                    quote=quote, author=real_author_db, contributed_by=contributed_by
                )
            else:
                quote_db = Quote.get(Quote.quote == quote)
            if new_author not in [a.author for a in Author.select()]:
                new_author_db = Author.create(
                    author=new_author, contributed_by=contributed_by
                )
            else:
                new_author_db = Author.get(Author.author == new_author)
            WrongQuote.create(
                quote=quote_db, author=new_author_db, contributed_by=contributed_by
            )
            flash(
                "Dein Zitat wurde gespeichert! Sobald es überprüft worden ist, wird es öffentlich sein."
            )
            session["email"] = request.form["email"]
            return redirect("/einreichen")
        return render_template("einreichen.html")

    @app.route("/rss")
    def rss():
        g.page = "top"

        quotes = sorted(
            list(WrongQuote.select()),
            key=lambda quote: quote.get_score(),
            reverse=True,
        )
        g.quotes = [
            (
                f'"{quote.quote.quote}" - {quote.author.author}',
                quote.get_score(),
                quote._pk,
            )
            for quote in quotes[:5]
        ]
        return Response(
            response=render_template("top.rss"),
            status=200,
            mimetype="application/rss+xml",
        )

    @app.route("/top")
    def top():
        g.page = "top"

        quotes = sorted(
            list(WrongQuote.select()),
            key=lambda quote: quote.get_score(),
            reverse=True,
        )
        g.quotes = [
            (f'"{quote.quote.quote}" - {quote.author.author}', quote.get_score(),)
            for quote in quotes[:5]
        ]
        return render_template("top.html")

    @app.route("/topall")
    def topall():
        g.page = "top"

        quotes = sorted(
            list(WrongQuote.select()),
            key=lambda quote: quote.get_score(),
            reverse=True,
        )
        g.quotes = [
            (
                f'"{quote.quote.quote}" - {quote.author.author}',
                round(quote.get_score() * 100),
            )
            for quote in quotes
        ]
        return render_template("top.html")

    @app.route("/zitate")
    def zitate():
        g.page = "zitate"
        g.quotes = [
            f'"{quote.quote.quote}" - {quote.author.author}'
            for quote in WrongQuote.select().where(WrongQuote.checked == True)
        ]
        return render_template("zitate.html")

    @app.route("/stats")
    def stats():
        g.page = "stats"
        g.votes = 0
        g.shows = 0
        g.quotes = 0
        quotes = list(WrongQuote.select())
        for quote in quotes:
            g.votes += quote.voted
            g.shows += quote.showed
            g.quotes += 1
        g.shows = g.shows / len(quotes)
        return render_template("stats.html")

    @app.route("/removecookies")
    def removecookies():
        session.clear()
        return redirect("/")

    return app

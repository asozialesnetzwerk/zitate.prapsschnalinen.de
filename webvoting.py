import os
from random import choice
from flask import Flask
from flask import (
    flash,
    g,
    redirect,
    render_template,
    request,
)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "voting.sqlite"),
    )
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from db import database, Quote

    @app.route("/hello")
    def hello():
        return "Hello, World"

    @app.route("/", methods=("GET",))
    def start():
        g.page = "start"
        if request.method == "POST":
            if 'zit' in request.form:
                voted, not_voted = request.form["zit"].split("-")
                voted_quote = Quote.get_by_id(int(voted))
                voted_quote.votes += 1
                voted_quote.shows += 1
                voted_quote.save()
                not_voted_quote = Quote.get_by_id(int(not_voted))
                not_voted_quote.shows += 1
                not_voted_quote.save()

        quotes = list(Quote.select().where(Quote.checked == True))
        quotes = sorted(quotes, key=lambda quote: quote.shows)
        final_quotes = []
        for quote in quotes:
            if quote.shows != quotes[-1].shows:
                final_quotes.append(quote)

        if len(final_quotes) == 1:
            final_quotes.append(choice(quotes.pop(quotes[0])))
        elif len(final_quotes) == 0:
            final_quotes = quotes

        zit1 = choice(final_quotes)
        zit2 = choice(final_quotes)
        while zit1 == zit2:
            zit1 = choice(final_quotes)
            zit2 = choice(final_quotes)

        g.zit1id = zit1._pk
        g.zit2id = zit2._pk
        g.zit1text = f'"{zit1.quote}" - {zit1.new_author}'
        g.zit2text = f'"{zit2.quote}" - {zit2.new_author}'
        return render_template("start.html")

    @app.route("/abstimmung", methods=("POST",))
    def abstimmung():
        if 'zit' in request.form:
            voted, not_voted = request.form["zit"].split("-")
            voted_quote = Quote.get_by_id(int(voted))
            voted_quote.votes += 1
            voted_quote.shows += 1
            voted_quote.save()
            not_voted_quote = Quote.get_by_id(int(not_voted))
            not_voted_quote.shows += 1
            not_voted_quote.save()
        return redirect('/')

    @app.route("/einreichen", methods=("GET", "POST"))
    def einreichen():
        g.page = "einreichen"
        if request.method == "POST":
            Quote.create(
                quote=request.form["quote"],
                new_author=request.form["wrongauthor"],
                real_author=request.form["realauthor"],
                contributed_by=request.form["email"],
            )
            flash("Dein Zitat wurde gespeichert! Sobald ich es überprüft hab, wird es Öffentlich sein.")
            return redirect("/")
        return render_template("einreichen.html")

    @app.route("/top")
    def top():
        g.page = "top"

        def get_sorting_factor(thing):
            if thing.shows == 0:
                return 0
            return thing.votes / thing.shows

        quotes = sorted(
            list(Quote.select()),
            key=lambda quote: quote.votes / quote.shows if quote.shows != 0 else 0,
            reverse=True,
        )
        g.quotes = [
            (
                f'"{quote.quote}" - {quote.new_author}',
                round(get_sorting_factor(quote) * 100),
            )
            for quote in quotes[:3]
        ]
        return render_template("top.html")

    @app.route("/zitate")
    def zitate():
        g.page = "zitate"
        g.quotes = [
            f'"{quote.quote}" - {quote.new_author}'
            for quote in Quote.select().where(Quote.checked == True)
        ]
        return render_template("zitate.html")

    @app.route("/stats")
    def stats():
        g.page = "stats"
        g.lines = []

        quotes = list(Quote.select())
        quotes = sorted(quotes, key=lambda quote: quote.shows)
        final_quotes = []
        for quote in quotes:
            if quote.shows != quotes[-1].shows:
                final_quotes.append(quote)

        if len(final_quotes) == 1:
            final_quotes.append(choice(quotes.pop(quotes[0])))
        elif len(final_quotes) == 0:
            final_quotes = quotes

        for quote in sorted(
            list(Quote.select()), key=lambda quote: quote.shows, reverse=True
        ):
            prfx = "*" if quote in final_quotes else "-"
            g.lines.append(prfx + "=" * quote.shows)
        return render_template("stats.html")

    return app

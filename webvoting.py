import os
from random import choice
from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'voting.sqlite'),
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
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

    @app.route("/", methods=('GET', 'POST'))
    def start():
        g.page = 'start'
        if request.method == "POST":
            voted, not_voted = request.form["zit"].split('-')
            voted_quote = Quote.get_by_id(int(voted))
            voted_quote.votes += 1
            voted_quote.shows += 1
            voted_quote.save()
            not_voted_quote = Quote.get_by_id(int(not_voted))
            not_voted_quote.shows += 1
            not_voted_quote.save()
        quotes = list(Quote.select())
        quotes = sorted(quotes, key=lambda quote: quote.shows)
        final_quotes = []
        for quote in quotes:
            if quote.shows != quotes[-1].shows:
                final_quotes.append(quote)

        if len(final_quotes) == 1:
            final_quotes.append(choice(quotes.pop(quotes[0])))


        zit1 = choice(final_quotes)
        zit2 = choice(final_quotes)
        while zit1 == zit2:
            zit1 = choice(final_quotes)
            zit2 = choice(final_quotes)

        g.zit1id = zit1._pk
        g.zit2id = zit2._pk
        g.zit1text = f'"{zit1.quote}" - {zit1.new_author}'
        g.zit2text = f'"{zit2.quote}" - {zit2.new_author}'
        return render_template('start.html')

    @app.route("/einreichen", methods=("GET", "POST"))
    def einreichen():
        g.page = 'einreichen'
        if request.method == 'POST':
            Quote.create(quote=request.form["quote"],
                         new_author=request.form['wrongauthor'],
                         real_author=request.form["realauthor"],
                         contributed_by=request.form["email"])
            g.note = "Dein Zitat wurde gespeichert!"
            return redirect("/")
        return render_template('einreichen.html')

    @app.route("/top")
    def top():
        g.page = 'top'
        def get_sorting_factor(thing):
            if thing.shows == 0:
                return 0
            print(thing.shows, thing.votes, thing.votes/thing.shows)
            return thing.votes/thing.shows
        quotes = sorted(list(Quote.select()), key=lambda quote: quote.votes/quote.shows if quote.shows != 0 else 0, reverse=True)
        print([(get_sorting_factor(quote), quote.new_author) for quote in quotes])
        g.quotes = [f'"{quote.quote}" - {quote.new_author}' for quote in quotes[:5]]
        return render_template('top.html')

    @app.route('/zitate')
    def zitate():
        g.page = 'zitate'
        g.quotes = [f'"{quote.quote}" - {quote.new_author}' for quote in Quote.select().where(Quote.checked == True)]
        return render_template('zitate.html')


    return app

from flask import Blueprint, jsonify
from db import WrongQuote, Quote, Author

api = Blueprint('/api', __name__, url_prefix='/api')


@api.route('/')
def docs():
    d = "GET /wrongquotes - get all wronguotes <br>" \
        "GET /wrongquotes/<id> - get wrongquote from id <br>" \
        "GET /wrongquotes/count - get wrongquote count <br><br>" \
        "GET /quotes - get all quotes <br>" \
        "GET /quotes/id - get quote from id <br>" \
        "GET /quotes/count - get quote count <br><br>" \
        "GET /authors - get all authors <br>" \
        "GET /authors/id - get author from id <br>" \
        "GET /authors/count - get author count"
    return d


@api.route('/wrongquotes')
def wrongquotes():
    quotes = []
    for quote in WrongQuote.select():
        quotes.append(quote.get_dict())
    return jsonify(quotes)


@api.route('/wrongquotes/<int:pk>')
def wrongquote(pk):
    return jsonify(WrongQuote.get_by_id(pk).get_dict())


@api.route('/wrongquotes/count')
def wrongquote_counts():
    return jsonify(len(WrongQuote.select()))


@api.route('/quotes')
def quotes():
    quotes = []
    for quote in Quote.select():
        quotes.append(quote.get_dict())
    return jsonify(quotes)


@api.route('/quotes/<int:pk>')
def quote(pk):
    return jsonify(Quote.get_by_id(pk).get_dict())


@api.route('/quotes/count')
def quote_count():
    return jsonify(len(Quote.select()))


@api.route('/authors')
def authors():
    quotes = []
    for quote in Author.select():
        quotes.append(quote.get_dict())
    return jsonify(quotes)


@api.route('/authors/<int:pk>')
def author(pk):
    return jsonify(Author.get_by_id(pk).get_dict())


@api.route("/authors/count")
def author_count():
    return jsonify(len(Author.select()))

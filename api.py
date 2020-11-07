from flask import Blueprint, jsonify, request
from db import WrongQuote, Quote, Author

api = Blueprint('/api', __name__, url_prefix='/api')


@api.route('/')
def docs():
    d = "GET /wrongquotes - get all wronguotes <br>" \
        "GET /wrongquotes/&ltid&gt - get wrongquote from id <br>" \
        "GET /wrongquotes/count - get wrongquote count <br>" \
        "POST /wrongquotes [quote: &ltquote_id&gt ; author: &ltauthor_id&gt ; contributed_by ; &ltcontributed_by&gt] - " \
        "add wrongquote to db <br><br>" \
        "GET /quotes - get all quotes <br>" \
        "GET /quotes/&ltid&gt - get quote from id <br>" \
        "GET /quotes/count - get quote count <br>" \
        "POST /quotes [quote: &ltquote&gt ; author: &ltauthor_id&gt] - add a quote to db <br><br>" \
        "GET /authors - get all authors <br>" \
        "GET /authors/&ltid&gt - get author from id <br>" \
        "GET /authors/count - get author count <br>" \
        "POST /authors [author: &ltauthor&gt] - add new author to db "
    return d


@api.route('/wrongquotes', methods=['GET', 'POST'])
def wrongquotes():
    if request.method == 'GET':
        wrongquotes = []
        for wrongquote in WrongQuote.select():
            wrongquotes.append(wrongquote.get_dict())
        return jsonify(quotes)
    elif request.method == 'POST':
        wrongquote = WrongQuote.create(quote=Quote.get_by_id(int(request.form['quote'])),
                                       author=Author.get_by_id(int(request.form['author'])),
                                       contributed_by=request.form['contributed_by'])
        return jsonify(wrongquote.get_dict())


@api.route('/wrongquotes/<int:pk>')
def wrongquote(pk):
    return jsonify(WrongQuote.get_by_id(pk).get_dict())


@api.route('/wrongquotes/count')
def wrongquote_counts():
    return jsonify(len(WrongQuote.select()))


@api.route('/quotes', methods=['GET', 'POST'])
def quotes():
    if request.method == 'GET':
        quotes = []
        for quote in Quote.select():
            quotes.append(quote.get_dict())
        return jsonify(quotes)
    elif request.method == 'POST':
        quote = Quote.create(quote=request.form['quote'],
                             author=Author.get_by_id(int(request.form['author'])))
        return jsonify(quote.get_dict())


@api.route('/quotes/<int:pk>')
def quote(pk):
    return jsonify(Quote.get_by_id(pk).get_dict())


@api.route('/quotes/count')
def quote_count():
    return jsonify(len(Quote.select()))


@api.route('/authors', methods=['GET', 'POST'])
def authors():
    if request.method == 'POST':
        author = Author.create(author=request.form['author'])
        return jsonify(author.get_dict())

    elif request.method == 'GET':
        authors = []
        for author in Author.select():
            authors.append(author.get_dict())
        return jsonify(authors)


@api.route('/authors/<int:pk>')
def author(pk):
    return jsonify(Author.get_by_id(pk).get_dict())


@api.route("/authors/count")
def author_count():
    return jsonify(len(Author.select()))



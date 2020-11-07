from flask import Blueprint, jsonify
from db import WrongQuote

api = Blueprint('api', __name__, url_prefix="/api/quotes")


@api.route('/')
def index():
    quotes = []
    for quote in WrongQuote.select():
        quotes.append(quote.get_dict())
    return jsonify(quotes)

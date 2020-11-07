from db import Author, Quote, WrongQuote
from db_old import Quote as Quote_old

for quote in Quote_old.select():
    if quote.real_author not in [a.author for a in Author.select()]:
        real_author = Author.create(author=quote.real_author)
    else:
        real_author = Author.get(Author.author == quote.real_author)
    if quote.quote not in [q.quote for q in Quote.select()]:
        quote_instance = Quote.create(quote=quote.quote, author=real_author)
    else:
        quote_instance = Quote.get(Quote.quote == quote.quote)
    if quote.new_author not in [a.author for a in Author.select()]:
        new_author = Author.create(author=quote.new_author)
    else:
        new_author = Author.get(Author.author == quote.new_author)
    WrongQuote.create(
        quote=quote_instance,
        author=new_author,
        voted=quote.votes,
        showed=quote.shows,
        checked=quote.checked,
        contributed_by=quote.contributed_by,
    )

from peewee import *
import peewee


database = SqliteDatabase("quotes.db")


class BaseModel(Model):
    class Meta:
        database = database


class Author(BaseModel):
    author = CharField()
    checked = BooleanField(default=False)
    contributed_by = CharField(null=True, default=None)

    def get_dict(self):
        return {"id": self._pk, "author": self.author}

    def get_or_create(author, checked=False, contributed_by=None):
        try:
            return Author.get(Author.author == author)
        except:
            with database.atomic():
                return Author.create(
                    author=author, checked=checked, contributed_by=contributed_by
                )


if not Author.table_exists():
    Author.create_table()


class Quote(BaseModel):
    quote = CharField()
    author = ForeignKeyField(Author, null=True)
    checked = BooleanField(default=False)
    contributed_by = CharField(null=True, default=None)

    def get_dict(self):
        return {"id": self._pk, "quote": self.quote, "author": self.author.get_dict()}

    def get_or_create(quote, author=None, checked=False, contributed_by=None):
        try:
            return Quote.get(
                self.quote == quote
            )  # I don't check if the author matches, also typos aren't accounted for.
        except:
            with database.atomic():
                if isinstance(author, str):
                    return Quote.create(
                        quote=quote,
                        author=Author.get_or_create(author),
                        checked=checked,
                        contributed_by=contributed_by,
                    )


if not Quote.table_exists():
    Quote.create_table()


class WrongQuote(BaseModel):
    quote = ForeignKeyField(Quote)
    author = ForeignKeyField(Author)
    voted = IntegerField(default=0)
    showed = IntegerField(default=0)
    rating = IntegerField(default=0)
    checked = BooleanField(default=False)
    contributed_by = CharField(null=True, default=None)

    def get_score(self):
        score = (self.voted + self.rating * 0.5) / self.showed if self.showed > 0 else 0
        if self.voted <= 5:
            score = score * 0.7
        return round(score * 100)

    def get_dict(self):
        return {
            "id": self._pk,
            "quote": self.quote.get_dict(),
            "author": self.author.get_dict(),
            "voted": self.voted,
            "showed": self.showed,
            "rating": self.rating,
            "checked": self.checked,
        }

    def get_or_create(
        quote,
        wrongauthor,
        realauthor=None,
        voted=0,
        showed=0,
        rating=0,
        checked=False,
        contributed_by=None,
    ):
        try:
            if isinstance(quote, str) and isinstance(
                wrongauthor, str
            ):  # only works for strings for now, I'll add more for db entries if I need them.
                WrongQuote.get(
                    WrongQuote.quote
                    == Quote.get_or_create(quote) & WrongQuote.author
                    == Author.get_or_create(wrongauthor)
                )
        except:
            if isinstance(wrongauthor, str):
                wrongauthor_db = Author.get_or_create(wrongauthor)
            if isinstance(quote, str):
                quote_db = Quote.get_or_create(quote, realauthor)
            with database.atomic():
                return WrongQuote.create(
                    quote=quote_db,
                    author=wrongauthor_db,
                    voted=voted,
                    showed=showed,
                    rating=rating,
                    checked=checked,
                    contributed_by=contributed_by,
                )


if not WrongQuote.table_exists():
    WrongQuote.create_table()

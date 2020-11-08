from peewee import *


database = SqliteDatabase("quotes.db")


class BaseModel(Model):
    class Meta:
        database = database


class Author(BaseModel):
    author = CharField()
    checked = BooleanField(default=False)
    contributed_by = CharField(null=True, default=None)

    def get_dict(self):
        return {'id': self._pk,
                'author': self.author}


if not Author.table_exists():
    Author.create_table()


class Quote(BaseModel):
    quote = CharField()
    author = ForeignKeyField(Author, null=True)
    checked = BooleanField(default=False)
    contributed_by = CharField(null=True, default=None)

    def get_dict(self):
        return {'id': self._pk,
                'quote': self.quote,
                'author': self.author.get_dict()}


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
        return self.voted/self.showed if self.showed > 0 else 0

    def get_dict(self):
        return {'id': self._pk,
                'quote': self.quote.get_dict(),
                'author': self.author.get_dict(),
                'voted': self.voted,
                'showed': self.showed,
                'checked': self.checked}


if not WrongQuote.table_exists():
    WrongQuote.create_table()





from peewee import *


database = SqliteDatabase("quotes.db")


class BaseModel(Model):
    class Meta:
        database = database


class Author(BaseModel):
    author = CharField()


if not Author.table_exists():
    Author.create_table()


class Quote(BaseModel):
    quote = CharField()
    author = ForeignKeyField(Author, null=True)


if not Quote.table_exists():
    Quote.create_table()


class WrongQuote(BaseModel):
    quote = ForeignKeyField(Quote)
    author = ForeignKeyField(Author)
    voted = IntegerField(default=0)
    showed = IntegerField(default=0)
    checked = BooleanField(default=False)
    contributed_by = CharField(null=True, default=None)


if not WrongQuote.table_exists():
    WrongQuote.create_table()





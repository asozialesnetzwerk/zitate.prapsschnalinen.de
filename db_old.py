from peewee import *

database_old = SqliteDatabase("quotes-old.db")


class Quote(Model):
    quote = CharField()
    new_author = CharField()
    real_author = CharField()
    contributed_by = CharField(null=True)
    votes = IntegerField(default=0)
    shows = IntegerField(default=0)
    checked = BooleanField(default=False)

    class Meta:
        database = database_old
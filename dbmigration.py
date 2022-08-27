from playhouse.migrate import *
from peewee import *
from db import Author, Quote, WrongQuote, database

migrator = SqliteMigrator(database)

migrate(
    migrator.add_column("WrongQuote", "score", IntegerField(default=0)),
)

for quote in WrongQuote.select():
    quote.save()

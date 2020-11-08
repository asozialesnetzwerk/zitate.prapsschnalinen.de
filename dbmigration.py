from playhouse.migrate import *
from peewee import *
from db import Author, Quote, WrongQuote, database

migrator = SqliteMigrator(database)

migrate(
    migrator.add_column('WrongQuote', 'rating', IntegerField(default=0)),
    migrator.add_column('Quote', 'contributed_by', CharField(null=True)),
    migrator.add_column('Quote', 'checked', BooleanField(default=False)),
    migrator.add_column('Author', 'contributed_by', CharField(null=True)),
    migrator.add_column('Author', 'checked', BooleanField(default=False))
)


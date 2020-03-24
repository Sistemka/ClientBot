from datetime import datetime as dt

from peewee import (
    CharField, DateTimeField, Model,
    IntegerField, PostgresqlDatabase, TextField
)
from playhouse.postgres_ext import ArrayField
import peeweedbevolve

from settings.config import PG_CONN

db = PostgresqlDatabase(**PG_CONN)


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    telegram_id = IntegerField(unique=True, primary_key=True)
    username = CharField(null=True)
    photos = ArrayField(TextField, default=[], null=True)
    created_dt = DateTimeField(default=dt.now)
    last_seen_dt = DateTimeField(default=dt.now)


if __name__ == '__main__':
    peeweedbevolve.evolve(db, interactive=False, ignore_tables=['basemodel'])

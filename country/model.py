from dataclasses import dataclass
from extensions import db


@dataclass
class Country(db.Model):

    id: int
    title: str

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), unique=True)


class CountryView(Country):

    total: int

    total = db.Column(db.Integer)
from flask import Flask
from extensions import db
from country.controller import country_controller


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/travel_agency"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JSON_AS_ASCII'] = False

app.register_blueprint(country_controller)

db.init_app(app)


if __name__ == '__main__':
    app.run()

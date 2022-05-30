from flask import Blueprint, request, make_response, jsonify, render_template, redirect
from sqlalchemy import text

from api_constants import *
from extensions import db
from .model import Country, CountryView


SECRET = 'administrator'


country_controller = Blueprint(
    'country_controller',
    __name__,
    template_folder='templates'
)


@country_controller.route(COUNTRY_GET_ALL_URL, methods=['GET'])
def get_all():
    query = text('SELECT * FROM country_agg_view')
    simple_query = text('SELECT * FROM country')
    if request.args.get("secret") == SECRET:
        countries = db \
            .session \
            .query(CountryView) \
            .from_statement(query) \
            .all()
        return render_template('country_all.html', data=countries)
    else:
        countries = db \
            .session \
            .query(Country) \
            .from_statement(simple_query) \
            .all()
        return render_template('country_all_simple.html', data=countries)


@country_controller.route(COUNTRY_GET_URL, methods=['GET'])
def get(c_id):
    query = text('SELECT * FROM country_get_by_id(:id)')
    country = db\
        .session\
        .query(Country)\
        .from_statement(query)\
        .params(id=c_id)\
        .all()
    return make_response(jsonify(country), 200)


@country_controller.route(COUNTRY_CREATE_URL, methods=['POST'])
def post():
    title = request.form['title']
    db.session.execute('CALL country_create(:title)', {"title": title})
    db.session.commit()
    return redirect(COUNTRY_GET_ALL_URL, code=200)


@country_controller.route(COUNTRY_DELETE_URL, methods=['POST'])
def delete(c_id):
    return _delete(c_id)


def _delete(c_id):
    db.session.execute('CALL country_delete(:id)', {"id": c_id})
    db.session.commit()
    return redirect(COUNTRY_GET_ALL_URL, code=200)

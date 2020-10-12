"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
import openaq
import requests
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/parent/Desktop/Unit3-sc3/airquality.sqlite3'
DB = SQLAlchemy(APP)

api = openaq.OpenAQ()
status, body = api.measurements(city='Los Angeles', parameter='pm25')
results = body['results']

tup= []
tup_list = []
for n in results:
    x = n['date']['utc']
    y = n['value']>=10
    tup.append(x)
    tup_list.append(y)
    m_list = [(tup[i], tup_list[i]) for i in range(0, len(tup))]


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f"<Record {self.id} {self.datetime}>"
print(m_list)

@APP.route('/')
def root():
    """Base view."""
    return str(m_list)


@APP.route('/refresh', methods=['GET'])
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    for n in m_list:
        db_date = n[0]
        db_value = n[1]
        new_rec = Record(datetime=db_date, value=db_value)
        DB.session.add(new_rec)
    DB.session.commit()
    return 'Data refreshed!'
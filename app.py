from flask import Flask, request, jsonify, render_template, make_response
from pymongo import MongoClient
import json
from bson import ObjectId
import scheduler.data_fetch as data_fetch


#serialization of any Python object while performing encoding
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# assigning the name of the flask application to the var app
app = Flask(__name__)
app.config["DEBUG"] = True

# batch process that fetches data from the our source url
#data_fetch.fetch_data()


# Home or Default Page
@app.route('/', methods=['GET'])
def get_total_cases_pie():
    result = get_cases_total()
    return render_template('countries_chart.html', data=result)


# api/getallcountries - a page for getting all the countries
@app.route('/api/getallcountries', methods=['GET'])
def get_all_countries():
    db = get_mongo()
    collection = db['countries']
    result = []
    cursor = collection.find({})
    for d in cursor:
        result.append(d)
    data = JSONEncoder().encode(result)
    r = make_response(data)
    r.mimetype = 'application/json'
    return  render_template('countries_maps.html', data=r)


# page for getting a specific country
@app.route('/api/getcountry', methods=['GET'])
def get_a_country():
    country = request.args.get('country')
    db = get_mongo()
    collection = db['countries']
    cursor = collection.find_one({'country': country})
    data = JSONEncoder().encode(cursor)
    r = make_response(data)
    r.mimetype = 'application/json'
    return r

# page for getting a specific country
@app.route('/api/getcontinent', methods=['GET'])
def get_a_continent():
    continent = request.args.get('continent')
    db = get_mongo()
    collection = db['countries']
    result = []
    cursor = collection.find({'continent': continent})
    for d in cursor:
        result.append(d)
    data = JSONEncoder().encode(result)
    r = make_response(data)
    r.mimetype = 'application/json'
    return r

# route returns total cases active, recovered, deaths
@app.route('/api/gettotalcases', methods=['GET'])
def get_countries():
    result = get_cases_total()
    return jsonify(result)

def get_mongo():
    client = MongoClient(
        "mongodb+srv://tejas:tejas@pythonfinalprojectclust.jcjtq.azure.mongodb.net")
    db = client["covid"]
    return db


def get_cases_total():
    db = get_mongo()
    collection = db['countries']
    result = {
        'active': 0,
        'deaths': 0,
        'recovered': 0
    }
    cursor = collection.find({})
    for d in cursor:
        result['active'] = result['active'] + d['active']
        result['deaths'] = result['deaths'] + d['deaths']
        result['recovered'] = result['recovered'] + d['recovered']
    return result

if(__name__ == "__main__"):
    app.run()

# AIzaSyAAYesKOAeNraBCbq0gzg3qMnEvm0LOoJ0
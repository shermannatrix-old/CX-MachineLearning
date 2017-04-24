from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'cxmachinelearningdb'
app.config['MONGO_URI'] = 'mongodb://cxadminuser:cxuser2017@ds161960.mlab.com:61960/cxmachinelearningdb'

mongo = PyMongo(app)


@app.route('/customers', methods=['GET'])
def get_all_customers():
    customers = mongo.db.customers

    output = []

    for c in customers.find():
        output.append({'_id': c['_id'], 'first_name': c['first_name'],
                       'last_name': c['last_name'],
                       'date_of_birth': c['date_of_birth'],
                       'is_online': c['is_online']})

    return jsonify({'results': output})


@app.route('/customers/<first_name>', methods=['GET'])
def get_single_customer(first_name):
    customers = mongo.db.customers

    c = customers.find_one({'first_name': first_name})

    if c:
        output = {'first_name': c['first_name'], 'last_name': c['last_name'], 'is_online': c['is_online']}
    else:
        output = 'No results found'

    return jsonify({'result': output})


@app.route('/customers', methods=['POST'])
def add_customer():
    customers = mongo.db.customers

    first_name = request.json['first_name']
    last_name = request.json['last_name']
    date_of_birth = request.json['date_of_birth']
    is_new = request.json['is_new']
    country = request.json['country']
    city = request.json['city']
    is_online = request.json['is_online']

    customer_id = customers.insert({'first_name': first_name, 'last_name': last_name,
                                    'date_of_birth': date_of_birth, 'is_new': is_new,
                                    'country': country, 'city': city, 'is_online': is_online})

    new_customer = customers.find_one({'_id': customer_id})

    output = {'first_name': new_customer['first_name'], 'last_name': new_customer['last_name']}

    return jsonify({'result': output})


@app.route('/customers/update_online_status', methods=['POST'])
def update_online_status():
    customers = mongo.db.customers

    customer_id = request.json['id']
    customer = customers.find_one({'_id': customer_id})

    if customer:
        customers.update_one({'_id': customer_id}, {'$set': {'is_online': 'true'}})
        return jsonify({'response': 'Customer: ' + str(customer_id) + ' is now online.'})
    else:
        return jsonify({'response': 'Customer ' + str(customer_id) + ' not found.'})


if __name__ == '__main__':
    app.run(debug=True)

# jsonify is a method that takes in a dictionary and returns a json text
# render_template is used to return an HTML page from a flask API
from flask import Flask, jsonify, request, render_template

print(__name__)
# Created a flask object
app = Flask(__name__)

stores = [
    {
        'name': 'MyStore1',
        'items': [
            {
                'name': 'item11',
                'price': 100
            },
            {
                'name': 'item12',
                'price': 50
            }
        ]
    },
    {
        'name': 'MyStore2',
        'items': [
            {
                'name': 'item21',
                'price': 119
            },
            {
                'name': 'item22',
                'price': 67
            },
            {
                'name': 'item23',
                'price': 32
            }
        ]
    }
]


# What to do when home url is hit
# By default app.route is a get request
@app.route('/')
def home():
    # return "Hello, world!"
    # By default it will look into the templates folder
    return render_template('index.html')


# POST /store {name:} --> create new store
@app.route('/store', methods=['POST'])
def create_store():
    # This request is the one that was made to this endpoint
    # Here we are extracting the json data from the request that we received
    # get_json() method will automatically covert the json into python dictionary.
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    # Return the new store created.
    return jsonify(new_store)


# GET /store/<string:name> --> get all data for the given store
# the name in app.route should match with the parameter name in function below it.
@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': f"No store exists with the name {name}"})


# GET /store --> get all stores
@app.route('/store/')
def get_stores():
    return jsonify({'stores': stores})


# POST /store/<string:name>/item {name:, price:} --> create new item in the given store
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    new_item = {'name': request_data['name'], 'price': request_data['price']}
    for i, store in enumerate(stores):
        if store['name'] == name:
            stores[i]['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': f"No store exists with the name {name} and hence could not add the item."})


# GET /store/<string:name>/item --> get all items for the given store
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if name == store['name']:
            return jsonify({'items': store['items']})
    return jsonify({'message': f"No store exists with the name {name} and hence could not return any item."})


# Run the flask app
app.run(port=5000)

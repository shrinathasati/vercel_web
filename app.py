from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
# from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables from .env file
# load_dotenv()

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


client=MongoClient('mongodb+srv://shrinathasati111:sanu2526@cluster0.qogwrwf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db=client.get_database('manit')

def get_collection(collection_name):
    return db[collection_name]

@app.route('/products/<collection_name>', methods=['GET'])
def get_products_by_collection(collection_name):
    collection = get_collection(collection_name)
    products = list(collection.find())
    for product in products:
        product["_id"] = str(product["_id"])
    return jsonify(products), 200

@app.route('/products/search', methods=['GET'])
def search_products():
    query = request.args.get('q', '')
    collections = ['men', 'shirts', 'women']
    if query in collections:
        collection = get_collection(query)
        products = list(collection.find())
        for product in products:
            product["_id"] = str(product["_id"])
        return jsonify(products), 200
    # results = []

    # for collection_name in collections:
    #     collection = get_collection(collection_name)
    #     products = list(collection.find({
    #         "$or": [
    #             {"details": {"$regex": query, "$options": "i"}}
    #         ]
    #     }))
    #     for product in products:
    #         product["_id"] = str(product["_id"])
    #     results.extend(products)


    return jsonify("not found"), 200

if __name__ == '__main__':
    app.run(debug=True)

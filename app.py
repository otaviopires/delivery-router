import helpers.db as db
import helpers.utils as utils
import modules.router as router

from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome to the Delivery Router API"

@app.route("/deliveryman", methods=["POST"])
def create_deliveryman():
    deliveryman_id = request.json.get('deliverymanId')
    service_price = request.json.get('servicePrice')
    exclusive_stores = request.json.get('exclusiveStores')

    if not deliveryman_id or not service_price or not exclusive_stores:
        return jsonify({'error': 'Please provide deliverymanId, servicePrice and exclusiveStores'}), 400

    resp = db.create_deliveryman(deliveryman_id, service_price, exclusive_stores)

    return jsonify({
        'status': 'User created!',
        'deliverymanId': deliveryman_id,
        'servicePrice': service_price,
        'exclusiveStores': exclusive_stores,
        'resp': resp
    })

@app.route("/deliveryman/<string:deliveryman_id>")
def get_deliveryman(deliveryman_id):
    item = db.fetch_deliveryman(deliveryman_id)

    if not item:
        return jsonify({'error': 'Delivery man does not exist'}), 404

        
    result = utils.deserialize(item)
    
    return jsonify({
        'deliverymanId': result.get('sk').split("#")[1],
        'servicePrice': result.get('servicePrice'),
        'exclusiveStores': list(result.get('exclusiveStores'))
    })

@app.route("/deliverymen")
def get_all_deliverymen():
    items = db.fetch_deliverymen()
    if not items:
        return jsonify({'error': 'No deliverymen found'}), 404
    return jsonify({'items': items})

@app.route("/store", methods=["POST"])
def create_store():
    store_id = request.json.get('storeId')
    percentage = request.json.get('percentage')

    if not store_id or not percentage:
        return jsonify({'error': 'Please provide storeId, percentage'}), 400

    resp = db.create_store(store_id, percentage)

    return jsonify({
        'status': 'Store created!',
        'storeId': store_id,
        'percentage': percentage,
        'dynamoDBReturn': resp
    })

@app.route("/store/<string:store_id>")
def get_store(store_id):
    item = db.fetch_store(store_id)
    if not item:
        return jsonify({'error': 'Delivery man does not exist'}), 404
    
    result = utils.deserialize(item)
    return jsonify({
        'storeId': result.get('sk').split("#")[1],
        'percentage': result.get('percentage')
    })

@app.route("/stores")
def get_all_stores():
    items = db.fetch_stores()
    if not items:
        return jsonify({'error': 'No stores found'}), 404

    return jsonify({'items': items})

@app.route("/order", methods=["POST"])
def create_order():
    order_id = request.json.get('orderId')
    store_id = request.json.get('storeId')
    order_value = request.json.get('orderValue')

    if not order_id or not store_id or not order_value:
        return jsonify({'error': 'Please provide orderId, storeId and orderValue'}), 400

    resp = db.create_order(order_id, store_id, order_value)

    return jsonify({
        'status': 'Order created!',
        'orderId': order_id,
        'storeId': store_id,
        'orderValue': order_value,
        'dynamoDBReturn': resp
    })

@app.route("/store/<string:store_id>/order/<string:order_id>")
def get_order(store_id, order_id):
    item = db.fetch_order(store_id, order_id)
    if not item:
        return jsonify({'error': 'Order does not exist'}), 404
    
    result = utils.deserialize(item)    
    return jsonify({
        'storeId': result.get('sk').split("#")[1],
        'orderId': result.get('sk').split("#")[3],
        'orderValue': result.get('orderValue')
    })

@app.route("/orders")
def get_all_orders():
    items = db.fetch_orders()
    if not items:
        return jsonify({'error': 'No orders found'}), 404
    return jsonify({'items': items})

@app.route("/router/calculate")
def get_all_routes():
    return router.get_all_routes()

@app.route("/router/calculate/deliveryman/<string:deliveryman_id>")
def get_routes_by_deliveryman(deliveryman_id):
    args = request.args
    shared = True if "shared" in args and args["shared"] == 'true'else False
    return router.get_routes_by_deliveryman(deliveryman_id, shared)

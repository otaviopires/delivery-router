import helpers.db as db
import helpers.utils as utils

def route_orders_for_deliveryman(service_price, orders, stores, order_per_deliveryman):
    deliveryman_orders = []
    for order in orders[:round(order_per_deliveryman)]:
        store_id = order.get('sk').split('#')[1]
        order_id = order.get('sk').split('#')[3]
        store = [s for s in stores if store_id in s.get('sk').split('#')[1]][0]
        percentage = float(store.get('percentage'))
        order_value = float(order.get('orderValue'))
        final_payment =  service_price + order_value + (order_value * (percentage / 100))
        deliveryman_orders.append({
            "storeId": store_id,
            "orderId": order_id,
            "finalPayment": final_payment,
        })
        orders = list(filter(lambda i: i['sk'] != order.get('sk'), orders)) 
    return deliveryman_orders, orders

def route_for_deliverymen(deliverymen, stores, orders, order_per_deliveryman, result):
    for deliveryman in deliverymen:
        service_price = float(deliveryman.get('servicePrice'))
        deliveryman_orders, orders = route_orders_for_deliveryman(service_price, orders, stores, order_per_deliveryman)
        result[deliveryman.get('sk').split('#')[1]] = {"orders": deliveryman_orders}

def route_for_exclusive_deliverymen(deliverymen, exclusive_deliverymen, stores, orders, order_per_deliveryman, result):
    for deliveryman in exclusive_deliverymen:
        service_price = float(deliveryman.get('servicePrice'))
        deliveryman_exclusive_stores = deliveryman.get('exclusiveStores')
        orders_for_exclusive_deliveryman = []
        for store in deliveryman_exclusive_stores:
            orders_for_exclusive_deliveryman.extend([o for o in orders if store in o.get('sk').split('#')[1]])
        orders_for_exclusive_deliveryman = orders_for_exclusive_deliveryman[:round(order_per_deliveryman)]
        deliveryman_orders, orders = route_orders_for_deliveryman(service_price, orders_for_exclusive_deliveryman, stores, order_per_deliveryman)
        result[deliveryman.get('sk').split('#')[1]] = {"orders": deliveryman_orders}
        deliverymen = list(filter(lambda i: i['sk'] != deliveryman.get('sk'), deliverymen))
        return deliverymen, orders_for_exclusive_deliveryman

def find_exclusive_deliverymen(deliverymen):
    return [deliveryman for deliveryman in deliverymen if not "-1" in deliveryman.get('exclusiveStores')]

def get_all_routes():
    result = {}
    stores = db.fetch_stores()
    orders = db.fetch_orders()
    deliverymen = utils.deserialize(db.fetch_deliverymen())
    order_per_deliveryman = len(orders) / len(deliverymen)
    exclusive_deliverymen = find_exclusive_deliverymen(deliverymen)
    deliverymen, orders_for_exclusive_deliveryman = route_for_exclusive_deliverymen(deliverymen, exclusive_deliverymen, stores, orders, order_per_deliveryman, result)

    print(orders)

    for o in orders_for_exclusive_deliveryman:
        orders = list(filter(lambda i: i['sk'] != o.get('sk'), orders))

    print(orders)

    route_for_deliverymen(deliverymen, stores, orders, order_per_deliveryman, result)
    return result

def get_routes_by_deliveryman(deliveryman_id, shared):
    result = {}
    stores = db.fetch_stores()
    orders = db.fetch_orders()

    if shared:
        deliverymen_to_count = utils.deserialize(db.fetch_deliverymen())
        order_per_deliveryman = len(orders) / len(deliverymen_to_count)
    else:
        order_per_deliveryman = len(orders)

    deliveryman = utils.deserialize(db.fetch_deliveryman(deliveryman_id))
    deliverymen = [deliveryman]
    if not "-1" in deliveryman.get('exclusiveStores'):
        route_for_exclusive_deliverymen(deliverymen, deliverymen, stores, orders, order_per_deliveryman, result)
    else:
        route_for_deliverymen(deliverymen, stores, orders, order_per_deliveryman, result)
    return result


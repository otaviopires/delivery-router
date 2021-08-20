import os
import boto3

import helpers.utils as utils

DELIVERY_ROUTER_TABLE = os.environ['TABLE_NAME']
client = boto3.client('dynamodb')

def create_deliveryman(deliveryman_id, service_price, exclusive_stores):
    return client.put_item(
        TableName=DELIVERY_ROUTER_TABLE,
        Item={
            'pk': { 'S': 'DELIVERYMAN'},
            'sk': { 'S': 'DELIVERYMAN#'+deliveryman_id },
            'servicePrice': { 'S': service_price },
            'exclusiveStores': {'SS': exclusive_stores }
        }
    )

def fetch_deliveryman(deliveryman_id):
    resp = client.get_item(
        TableName=DELIVERY_ROUTER_TABLE,
        Key = {
            'pk': { 'S' : 'DELIVERYMAN' },
            'sk': { 'S' : 'DELIVERYMAN#'+deliveryman_id }
        }
    )
    return resp.get('Item')

def fetch_deliverymen():
    resp = client.query(
        TableName=DELIVERY_ROUTER_TABLE,
        KeyConditionExpression='pk = :pk AND begins_with ( sk , :sk )',
        ExpressionAttributeValues={
            ':pk': {'S': 'DELIVERYMAN'},
            ':sk': {'S': 'DELIVERYMAN#'}
        }
    )
    return resp['Items']

def create_store(store_id, percentage):
    return client.put_item(
        TableName=DELIVERY_ROUTER_TABLE,
        Item={
            'pk': { 'S': 'STORE' },
            'sk': { 'S': 'STORE#'+store_id },
            'percentage': { 'S': percentage }
        }
    )

def fetch_store(store_id):
    resp = client.get_item(
        TableName=DELIVERY_ROUTER_TABLE,
        Key = {
            'pk': { 'S' : 'STORE' },
            'sk': { 'S' : 'STORE#'+store_id }
        }
    )
    return resp.get('Item')

def fetch_stores():
    resp = client.query(
        TableName=DELIVERY_ROUTER_TABLE,
        KeyConditionExpression='pk = :pk AND begins_with ( sk , :sk )',
        ExpressionAttributeValues={
            ':pk': {'S': 'STORE'},
            ':sk': {'S': 'STORE#'}
        }
    )
    return utils.deserialize(resp['Items'])

def create_order(order_id, store_id, order_value):
    return client.put_item(
        TableName=DELIVERY_ROUTER_TABLE,
        Item={
            'pk': { 'S': 'STORE#ORDER' },
            'sk': { 'S': 'STORE#'+ store_id + '#ORDER#' + order_id },
            'orderValue': { 'S': order_value }
        }
    )

def fetch_order(store_id, order_id):
    resp = client.get_item(
        TableName=DELIVERY_ROUTER_TABLE,
        Key = {
            'pk': { 'S' : 'STORE#ORDER' },
            'sk': { 'S' : 'STORE#'+ store_id + '#ORDER#' + order_id }
        }
    )
    return resp.get('Item')

def fetch_orders():
    resp = client.query(
        TableName=DELIVERY_ROUTER_TABLE,
        KeyConditionExpression='pk = :pk',
        ExpressionAttributeValues={
            ':pk': {'S': 'STORE#ORDER'}
        }
    )
    return utils.deserialize(resp['Items'])
    

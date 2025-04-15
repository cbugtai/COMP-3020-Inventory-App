import json
import boto3
import ulid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    item = {
        'item_id': str(ulid.new()),
        'item_name': body['item_name'],
        'item_description': body['item_description'],
        'item_qty': int(body['item_qty']),
        'item_price': float(body['item_price']),
        'location_id': int(body['location_id'])
    }
    table.put_item(Item=item)
    return {
        'statusCode': 201,
        'body': json.dumps({'message': 'Item added', 'item': item})
    }

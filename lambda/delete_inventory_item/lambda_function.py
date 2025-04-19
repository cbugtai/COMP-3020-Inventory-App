import simplejson as json
import boto3
from boto3.dynamodb.conditions import Key

# Updated Function, now tested and confirmed works

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Define the DynamoDB table name
TABLE_NAME = 'Inventory'

def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)

    path_params = event.get('pathParameters') or {}
    item_id = path_params.get('id')

    try:
        # Query to get all items with item_id = :id
        response = table.query(
            KeyConditionExpression=Key('item_id').eq(item_id)
        )
        items = response.get('Items', [])

        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps('Item not found')
            }

        # Delete all items with item_id = :id
        for item in items:
            table.delete_item(
                Key={
                    'item_id': item['item_id'],
                    'location_id': item['location_id']
                }
            )
        
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with item_id '{item_id}' deleted successfully.")
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting item: {str(e)}")
        }
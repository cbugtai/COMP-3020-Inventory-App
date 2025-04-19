import simplejson as json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

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
    except ClientError as e:
        print(f"Failed to query items: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to query items')
        }

    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }
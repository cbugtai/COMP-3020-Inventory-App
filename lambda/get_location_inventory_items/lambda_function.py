import simplejson as json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Define the DynamoDB table name
TABLE_NAME = 'Inventory'

def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)

    try:
        # Query to get all items with PK = "location_id"
        response = table.query(
            KeyConditionExpression=Key('PK').eq('location_id')
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
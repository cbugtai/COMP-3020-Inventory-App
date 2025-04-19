import boto3
import json

# Updated Function, now tested and confirmed works

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    path_params = event.get('pathParameters') or {}
    location_id = path_params.get('id')

    if not location_id:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'location_id' path parameter")
        }

    try:
        response = table.query(
            IndexName='GSI',
            KeyConditionExpression=boto3.dynamodb.conditions.Key('location_id').eq(int(location_id))
        )
        items = response.get('Items', [])

        return {
            'statusCode': 200,
            'body': json.dumps(items, default=str)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error retrieving items: {str(e)}")
        }
import boto3
import json
import os

print('Loading function')

dynamo = boto3.resource('dynamodb')
table = dynamo.Table("{}-{}-{}-{}-dynamo".format(
    os.environ['PIPELINE_PORTFOLIO'],
    os.environ['PIPELINE_APP']
))


def handler(event, context):
    print({"os.environ": json.dumps(os.environ)})

    operation = event['operation']
    id = event['id']

    if operation == 'write':
        value = event['value']
        response = table.put_item(
            Item={
                'id': id,
                'value': value
            }
        )
        return {
            "Status": "OK"
        }

    elif operation == 'read':
        response = table.get_item(
            Key={
                'id': id
            }
        )

        if 'Item' in response:
            return {
                "Status": "OK",
                "Item": response["Item"]
            }
        else:
            raise Exception("No such item")

    elif operation == 'delete':
        response = table.delete_item(
            Key={
                'id': id
            }
        )

        return {}
    else:
        print("Unknown operation '{}'".format(operation))


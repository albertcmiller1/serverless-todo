import json
from urllib import response
import boto3
import logging 
import requests
from decimal import Decimal 

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodbTableName = 'TestTable'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

getMethod = 'GET'
postMethod = 'POST'
patchMethod = 'PATCH'
deleteMethod = 'DELETE'

healthPath = '/health'
productPath = '/product'
productsPath = '/products'

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    logger.info("## EVENT:")
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']

    if httpMethod == getMethod and path == healthPath:
        response = buildResponse(200)
    elif httpMethod == getMethod and path == productPath:
        response = getProduct(event['queryStringParameters']['productId'])
    elif httpMethod == getMethod and path == productsPath: 
        response = getProducts()
    elif httpMethod == postMethod and path == productPath: 
        response = saveProduct(json.loads(event['body']))
    elif httpMethod == patchMethod and path == productPath: 
        requestBody = json.loads(event['body'])
        response = modifyProduct(requestBody['productId'], requestBody['updateKey'], requestBody['updateValue'])
    elif httpMethod == deleteMethod and path == productPath: 
        requestBody = json.loads(event['body'])
        response = deleteProduct(requestBody['productId'])
    else: 
        # response = buildResponse(404, "Not Found")
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "hello world with change!",
                # "location": ip.text.replace("\n", "")
            }),
        }

    return response


def getProduct(productId): 
    try: 
        response = table.get_item(
            Key={
                'productId': productId
            }
        )
        if 'Item' in response: 
            return buildResponse(200, response['Item'])
        else: 
            return buildResponse(404, {'Message': 'ProductId: %s not found' % productId})
    except: 
        logger.exception("something went wrong in the getProduct() method")



def getProducts():
    try: 
        response = table.scan()
        result = response['Items']

        while 'LastEvaluatedKey' in response: 
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            result.extend(response['Items'])
        
        body = {
            'products': response
        }
        return buildResponse(200, body)
    except: 
        logger.exception("something went wrong in getProducts() method")



def saveProduct(requestBody): 
    try: 
        logger.info("starting saveProduct() function")
        table.put_item(Item=requestBody)
        logger.info("## REQUEST BODY")
        logger.info(requestBody)
        body = {
            'Operation': 'SAVE', 
            'Message': 'SUCCESS', 
            'Item': requestBody
        }
        return buildResponse(200, body)
    except: 
        logger.exception("something went wrong in saveProduct() method")


def modifyProduct(productId, updateKey, updateValue): 
    try: 
        response = table.update_item(
            Key={
                'productId': productId
            },
            UpdateExpression='set %s = :value' % updateKey, 
            ExpressionAttributeValues={
                ':value': updateValue
            },
            ReturnValues='UPDATED_NEW'
        )
        body = {
            'Operation': 'UPDATE',
            'Message': 'SUCCESS',
            'UpdatedAttrebutes': response
        }
        return buildResponse(200, body)
    except: 
        logger.exception("something went wrong in modifyProduct() method")


def deleteProduct(productId):
    try: 
        response = table.delete_item(
            Key={
                'productId': productId
            },
            ReturnValues='ALL_OLD'
        )
        body = {
            'Operation': 'DELETE',
            'Message': 'SUCCESS',
            'deletedItem': response
        }
        return buildResponse(200, body)
    except: 
        logger.exception("something went wrong in deleteProduct() method")


def buildResponse(statusCode, body=None): 
    logger.info("MADE IT TO buildRespose FUNCTION")
    response = {
        'statusCode': statusCode, 
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None: 
        response['body'] = json.dumps(body, cls=CustomEncoder)
    logger.info("## RESPONSE ")
    logger.info(response)
    return response


# object we get from dynamo is in decimal 
# decimal is not supported by json encoder 
class CustomEncoder(json.JSONEncoder): 
    def default(self, obj): 
        if isinstance(obj, Decimal): 
            return float(obj)
        return json.JSONEncoder.default(self, obj)

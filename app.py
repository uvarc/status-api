from chalice import Chalice, Response
import json
import time
import sys
import os
import datetime
import random
import string
from decimal import Decimal
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

app = Chalice(app_name='status-badges')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('status')

os.chdir("/tmp")

def sort_list(items):
    return items['partition']

def sort_system(items):
    return items['sort']

@app.route('/badge/{syst}', methods=['GET'], cors=True)
def badge_status(syst):
    payload = {}
    try:
        response = table.query(
            KeyConditionExpression=Key('system').eq(syst)
        )
        result = response['Items'][0]
        title = result['title']
        statez = int(result['statez'])
        color = result['color']
        message = result['message']
        payload = {"schemaVersion":1,"label":title,"message": message,"color":color}
        return payload
    except ClientError as error:
        raise error

# @app.route('/anybadge/{syst}', methods=['GET'], cors=True)
# def return_badge(syst):
#     try:
#         file = syst + ".svg"
#         response = table.query(
#             KeyConditionExpression=Key('system').eq(syst)
#         )
#         result = response['Items'][0]
#         title = result['title']
#         statez = int(result['statez'])
#         # color = result['color']
#         color = 'red'
#         message = result['message']
#         payload = {"schemaVersion":1,"label":title,"message": message,"color":color}
#         img_data = Badge(label='TESTING', value=color, default_color=color).write_badge(file, overwrite=True)
#         # img_data = Badge(label="TESTING", value=color, default_color=color).write_badge
#         return Response(body=img_data, status_code=200, headers={'Content-Type': 'image/png'})
#     except ClientError as error:
#         raise error


@app.route('/grid', methods=['GET'], cors=True)
def status_grid():
    table = dynamodb.Table('status')
    try:
        state = []
        stat = table.scan()
        for j in stat[u'Items']:
            state.append(j)
            state.sort(key=sort_system)
        return state
    except ClientError as error:
        raise error

@app.route('/messages', methods=[ 'GET'], cors=True)
def get_messages():
    table = dynamodb.Table('status-messages')
    messages = []   
    msgs = table.scan()
    for j in msgs[u'Items']:  
      messages.append(j)
    try:
        return messages
    except Exception as e:
        return response({'message': e.message}, 400)


@app.route('/accord/messages', methods=[ 'GET'], cors=True)
def get_accord_messages():
    table = dynamodb.Table('accord-messages')
    messages = []   
    msgs = table.scan()
    for j in msgs[u'Items']:  
      messages.append(j)
    try:
        return messages
    except Exception as e:
        return response({'message': e.message}, 400)


@app.route('/accord/messages', methods=[ 'POST'])
def post_accord_message():
    table = dynamodb.Table('accord-messages')
    payload = app.current_request.json_body
    print(payload)
    # We'll echo the json body back to the user in a 'user' key.
    body = payload['message']
    try:
        update_this = table.update_item(
            Key={
                'message': 'message'
            },
            UpdateExpression="set message=:m, body=:b",
            ExpressionAttributeValues={
                ':m': 'message',
                ':b': body
            }
        )
    except Exception as e:
        return {'exception': e.message}


@app.route('/persona/{pkey}', methods=['GET'], cors=True)
def hello_name(pkey):
    try:
        client = boto3.client("dynamodb")
        response = client.query(
            TableName='persona',
            KeyConditionExpression='pkey = :pkey',
            ExpressionAttributeValues={
                ':pkey': {'S': pkey}
            }
        )
        if response['Count'] > 0:
            uid = response['Items'][0]['puid']['S']
            name = response['Items'][0]['pname']['S']
            fname = response['Items'][0]['pfname']['S']
            lname = response['Items'][0]['plname']['S']
            eppn = response['Items'][0]['peppn']['S']
            return { "uid":uid,"name":name,"fname":fname,"lname":lname,"eppn":eppn}
        else:
            return { "status": "Error. No record found" }
    except Exception as e:
        return response({'message': e.message}, 400)

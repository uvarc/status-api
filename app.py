from chalice import Chalice
import json
import time
import sys
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


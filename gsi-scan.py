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

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('status')

def sort_list(items):
    return items['partition']

def sort_system(items):
    return items['sort']

def status_grid():
    table = dynamodb.Table('status')
    try:
        state = []
        stat = table.scan(IndexName='system-sort-index')
        for j in stat[u'Items']:
            state.append(j)
            # state.sort(key=sort_system)
        # return state
        print(state)
    except ClientError as error:
        raise error

status_grid()
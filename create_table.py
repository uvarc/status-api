import boto3

def create_movie_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.create_table(
        TableName='statusZZ',
        KeySchema=[
            {
                'AttributeName': 'system',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'sort',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'system',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'sort',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    return table


if __name__ == '__main__':
    status = create_movie_table()
    print("Table status:", status.table_status)
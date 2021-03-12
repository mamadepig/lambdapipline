import json
import boto3
import requests

def search_photo(object_list):
    results = []
    for i in range(len(object_list)):
        print(object_list[i])
        if object_list[i] == None:
            continue
        object = object_list[i].lower()
        url = 'https://search-photos-u6qba4mer7yenbxzvpn6a7ociu.us-west-2.es.amazonaws.com/photos/_search?q=labels:'
        response = json.loads(requests.get(url + '"' + object + '"', auth = ('jiayuanguo', '201006004@aAa')).text)
        for result in response['hits']['hits']:
            results.append(result)
    return results

def lambda_handler(event, context):
    # TODO implement
    print(event)
    q = event['queryStringParameters']['q']
    print(q)
    client = boto3.client('lex-runtime')
    response = client.post_text(
        botName = 'SearchPhotoBot',
        botAlias = 'searchbot',
        userId = 'mamadepig',
        sessionAttributes={
            },
        requestAttributes={
        },
        inputText = q
    )
    print(response)
    objectOne = response['slots']['objectOne']
    objectTwo = response['slots']['objectTwo']
    print(objectOne, objectTwo)
    r = search_photo([objectOne, objectTwo])
    print(r)
    response = {
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body':json.dumps({
            'result':[{
            'url': 'https://myphotosbuck.s3-us-west-2.amazonaws.com/' + res['_source']['objectKey'],
            'labels': res['_source']['labels']
        } for res in r]}),
        'statusCode': 200,
        
    }
    return response

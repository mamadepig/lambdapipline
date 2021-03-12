import json
import boto3
import requests
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection

def get_label(bucket, photo):
    client = boto3.client('rekognition')
    response = client.detect_labels(
        Image = {
            'S3Object':{
                'Bucket': bucket,
                'Name': photo
            }
        },
        MaxLabels=5,
        MinConfidence = 0.7
        )
    labels = []
    for item in response['Labels']:
        labels.append(item['Name'].lower())
    return labels

def lambda_handler(event, context):
    # TODO implement
    print(event)
    bucket = event['Records'][0]['s3']['bucket']['name']
    photo = event['Records'][0]['s3']['object']['key']
    time_stamp = event['Records'][0]['eventTime']
    labels = get_label(bucket, photo)
    print(labels)
    s3 = boto3.resource('s3')
    object = s3.Object(bucket, photo)
    print(type(object.metadata))
    print(object.metadata)
    mylabel = object.metadata['customlabels'].split(',')
    for label in mylabel:
        labels.append(label)
    print(mylabel)
    #print(object.content_type)
    host = 'https://search-photos-u6qba4mer7yenbxzvpn6a7ociu.us-west-2.es.amazonaws.com'
    url = host + '/photos/pics'
    document = {
                'objectKey': photo,
                'bucket': bucket,
                'createdTimestamp': time_stamp,
                'labels': labels
                }
    #print(document)
    headers = { "Content-Type": "application/json" }
    r = requests.post(url, auth=('jiayuanguo', '201006004@aAa'), json=document, headers=headers)
    #print(r.text)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

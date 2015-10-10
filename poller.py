import boto3
import subprocess
import datetime

QUEUE_URL = "https://queue.amazonaws.com/829315242464/button_events"
last_deletion = datetime.datetime.now()
sqs = boto3.client("sqs")

while True:
    response = sqs.receive_message(QueueUrl=QUEUE_URL, WaitTimeSeconds=20,
        MaxNumberOfMessages=1)

    if "Messages" in response:
        message = response["Messages"][0]
        print message

        del_response = sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=message['ReceiptHandle'])

    else:
        print "No messages"

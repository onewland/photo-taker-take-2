import boto3
import subprocess
import datetime
import glob
import time
import os

QUEUE_URL = "https://queue.amazonaws.com/829315242464/button_events"
SNAPSHOT_GLOB = 'snapshot-[0-9]*.jpg'

last_deletion = time.time()
sqs = boto3.client("sqs")

def clean_old_snapshots():
    global last_deletion

    time_diff = time.time() - last_deletion
    if time_diff > 20:
        files = glob.glob(SNAPSHOT_GLOB)
        [os.remove(fname) for fname in files]
        last_deletion = time.time()

while True:
    response = sqs.receive_message(QueueUrl=QUEUE_URL, WaitTimeSeconds=20,
        MaxNumberOfMessages=1)

    if "Messages" in response:
        message = response["Messages"][0]
        print message

        files = glob.glob(SNAPSHOT_GLOB)[-4:]

        if len(files) == 4:
            filenames_trimmed = [os.path.splitext(fname)[0] for fname in files]
            subprocess.call(["./transform.sh"] + filenames_trimmed)
        else:
            print "Glitchy response"

        del_response = sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=message['ReceiptHandle'])

    else:
        print "No messages"

    clean_old_snapshots()

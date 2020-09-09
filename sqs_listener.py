import json
import boto3
import time
from datetime import date
import presigned_url_client

class SQSListener:
    def __init__(self, queue_url):
        self.queue_url = queue_url


    def __str__(self):
        return "I am the SQS listener. My queue URL is {0}".format(self.queue_url)


    """
    message should be a json string
    """
    def send_message(self, message):
        sqs = boto3.client('sqs')
        send_message_response = sqs.send_message(
            QueueUrl=self.queue_url,
            DelaySeconds=1,
            MessageBody=(message)
        )
        return send_message_response["MessageId"]

    def listen(self):
        sqs = boto3.client('sqs')
        while True:
            response = sqs.receive_message(
                QueueUrl=self.queue_url,
                AttributeNames=[
                    'SentTimestamp'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ],
                WaitTimeSeconds=20
            )
            if "Messages" in response:
                print("Received a message")
                messages = response["Messages"]
                for message in messages:
                    receipt_handle = message["ReceiptHandle"]
                    message_body = message["Body"]
                    message_body_json = json.loads(message_body)
                    print(message_body_json)
                    is_success = self.onReceiveMessage(message_body_json)
                    sqs.delete_message(
                        QueueUrl=self.queue_url,
                        ReceiptHandle=receipt_handle
                    )
                    print("Deleting message")


    def onReceiveMessage(self, message):
        """
        code to process document and upload results to S3. return true if success, false otherwise
        """
        print("Processing message")
        return True 

    
    "Only used for testing purposes. Use to send mock message to queue"
    def send_mock_message(self):
        client = presigned_url_client.PresignedUrlClient()
        mock_message_json = {
            "messageId": "abc123",
            "messageDate": str(date.today()),
            "type": "OCR_PROCESS",
            "docId": "doc123",
            "documentDownloadUrl": client.create_presigned_download_url("thanh-assignment-bucket", "ParticipationGrade.pdf"),
            "contentType": "application/pdf",
            "fileSizeInBytes": "69000",
            "shaChecksum": "fakeCheckSum",
            "metadata": {
                "ocrUploadUrl": client.create_presigned_upload_url("thanh-assignment-bucket", "ocr.pdf"),
                "searchablePdfUploadUrl": client.create_presigned_upload_url("thanh-assignment-bucket", "searchable.pdf"),
                "boundingBoxUploadUrl": client.create_presigned_upload_url("thanh-assignment-bucket", "bb.pdf"),
                "pdfUploadUrl": "fakeUrl",
                "numberOfPages": "1",
            } 
        }
        mock_message_string = json.dumps(mock_message_json)
        self.send_message(mock_message_string)



    "Only used for testing purposes. Use to initially create SQS queue"
    def create_queue(self, queue_name):
        sqs = boto3.resource('sqs')
        queue = sqs.create_queue(QueueName=queue_name, Attributes={'DelaySeconds': '1'})
        self.queue_url = queue.url
        return queue.url
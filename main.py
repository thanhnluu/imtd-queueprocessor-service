import presigned_url_client
import sqs_listener

if __name__ == "__main__":
   """
   # File upload and download with presigned urls
   client = presigned_url_client.PresignedUrlClient()
   upload_url = client.create_presigned_upload_url("thanh-assignment-bucket", "ParticipationGrade.pdf")
   print("Upload URL: {0}".format(upload_url))
   client.upload_file(upload_url, "test_files/ParticipationGrade.pdf")
   print("File successfully uploaded")
   download_url = client.create_presigned_download_url("thanh-assignment-bucket", "ParticipationGrade.pdf")
   print("Download URL: {0}".format(download_url))
   client.download_file(download_url, "test_files/download_ParticipationGrade.pdf")
   """

   # sqs_client = sqs_listener.SQSListener("blah")
   # queue_url = sqs_client.create_queue("thanh-test-queue")
   sqs_client = sqs_listener.SQSListener("https://sqs.us-east-1.amazonaws.com/242071178326/thanh-test-queue")
   print("listening...")
   sqs_client.listen()
   print("done listening")

   #sqs_client.send_mock_message()
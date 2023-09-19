# This is a Lambda function that looks triggers an SNS notification when a file is uploaded to an S3 bucket. The notification contains a pre-signed URL that allows the
# recipient to download the file from the S3 bucket. This method is more secure than the deprecated method of sending an email notification using the AWS Simple Email
# Service (SES) because the notification is sent from Amazon rather than an external email account.

# Trigger: S3
# Bucket arn: <redacted>
# Prefix: apis/eloqua/webformsummary

import boto3

topic_arn = "<redacted>"

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except Exception as e:
        print("Error generating pre-signed URL: ", e)
        return None
    return response

def send_sns(message, subject):
    try:
        client = boto3.client("sns")
        result = client.publish(TopicArn=topic_arn, Message=message, Subject=subject)
        if result['ResponseMetadata']['HTTPStatusCode'] == 200:
            print(result)
            print("Notification sent successfully..!!!")
            return True
    except Exception as e:
        print("Error occurred while publishing notifications, and the error is: ", e)
        return False

def lambda_handler(event, context):
    print("Event collected is {}".format(event))
    for record in event['Records']:
        s3_bucket = record['s3']['bucket']['name']
        s3_key = record['s3']['object']['key']
        
        # Generate a pre-signed URL for downloading the file
        download_link = generate_presigned_url(s3_bucket, s3_key)
        if download_link is None:
            print("Failed to generate pre-signed URL.")
            return False

        # Custom message for the notification
        message = (
            f"This is an automated generated email from Amazon Simple Notification Service (SNS).\n\n"
            "This email is to notify you that Eloqua records have successfully been processed into the Azure Service Bus. "
            "A copy of these records has been uploaded to the databricks-keb-shard/apis/eloqua/ S3 directory under the keb-tds AWS account. "
            f"Please download this week's summary report using the link provided below:\n\n"
            f"Download Link: {download_link}\n\n"
            "If you have any questions or concerns, please reach out to <redacted> via email at <redacted>."
        )

        # Custom subject for the notification
        subject = "Notification: Eloqua records have successfully been processed"

        SNSResult = send_sns(message, subject)
        if SNSResult:
            print("Notification Sent..") 
            return SNSResult
        else:
            return False

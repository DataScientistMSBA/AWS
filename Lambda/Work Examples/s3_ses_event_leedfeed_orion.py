# This is a redacted deprecated Lambda function script that I developed for work that sends an email notification to a list of recipients when a file is uploaded to 
# an S3 bucket from an external scheduled job. The email contained a copy of the file that was uploaded to the S3 bucket as an attachment. The email was sent using 
# the AWS Simple Email Service (SES).This method was replaced by a Simple Notification Service (SNS) topic that sends an email to a list of recipients when a file 
# is uploaded to an S3 bucket because it is more secure to have the notification come from Amazon rather then an external email account. Using our internal email 
# domains were automatically being flagged as possible phishing attacks by our internal email server.

# Trigger: S3
# Bucket arn: <redacted>
# Prefix: apis/eloqua/temp/

import boto3
import io
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def lambda_handler(event, context):
    ses = boto3.client("ses")
    s3 = boto3.client("s3")

    for i in event["Records"]:
        bucket_name = i["s3"]["bucket"]["name"]
        object = i["s3"]["object"]["key"]

    fileObj = s3.get_object(Bucket=bucket_name, Key=object)
    file_content = fileObj["Body"].read()

    sender = "<redacted>"
    # to = ["<redacted>", "<redacted>"]

    subject = "Notification: Eloqua records have successfully been processed"
    body = f"""
        <br>
        This is an automated generated email from Amazon Simple Email Service (SES).
        <br>
        <br>
        This email is to notify you that Eloqua records have successfully been processed into the Azure Service Bus.
        A copy of these records has been uploaded to the {bucket_name}/{object} S3 directory under the <redacted> AWS account. Attached is a copy for your records.
        <br>
        <br>
        If you have any questions or concerns, please reach out to <redacted> via email at "<redacted>".
    """

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(to)  # Join the email addresses with commas

    body_txt = MIMEText(body, "html")

    attachment = MIMEApplication(io.BytesIO(file_content).read())
    attachment.add_header("Content-Disposition", "attachment", filename="LeadFeedOrion_Results.csv")

    msg.attach(body_txt)
    msg.attach(attachment)

    response = ses.send_raw_email(Source=sender, Destinations=to, RawMessage={"Data": msg.as_string()})

    return "Thanks"

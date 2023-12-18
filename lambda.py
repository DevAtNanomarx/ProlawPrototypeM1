import boto3
import base64
import datetime
import json
import os

s3 = boto3.client('s3')
textract = boto3.client('textract')

OUTPUT_BUCKET = os.getenv('OUTPUT_BUCKET') or 'prolaw-prototype-m1-bucket'

def lambda_handler(event, context):
    # Decode the base64 encoded PDF
    data = json.loads(event['body'])
    pdf_data = base64.b64decode(data['doc'])

    base_filename, file_extension = os.path.splitext(data['filename'])

    # Generate a filename with the current datetime
    filename = 'uploads/' + base_filename + '_' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + file_extension

    # Upload the PDF to S3
    s3.put_object(Body=pdf_data, Bucket=OUTPUT_BUCKET, Key=filename)

    # Use Textract to analyze the PDF
    response = textract.analyze_expense(Document={'S3Object': {'Bucket': OUTPUT_BUCKET, 'Name': filename}})

    # Format the result as JSON and store it in 'results'
    result_filename = 'results/' + base_filename + '_' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + '.json'
    s3.put_object(Body=json.dumps(response), Bucket=OUTPUT_BUCKET, Key=result_filename)

    # Return the result
    return response
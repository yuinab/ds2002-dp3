import boto3
from botocore.exceptions import ClientError

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/ncd6fc"
sqs = boto3.client('sqs')

def delete_message(handle):
    try:
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])

def process_messages():
    messages = []  
    phrase = '' 
    try:
        while True:
            # Receive messages from SQS queue. Each message has two MessageAttributes: order and word
            response = sqs.receive_message(
                QueueUrl=url,
                AttributeNames=[
                    'All'
                ],
                MaxNumberOfMessages=10,  # Retrieve 10 messages at once
                MessageAttributeNames=[
                    'All'
                ]
            )
           
            # Check if there are messages in the queue or not
            if "Messages" in response:
                for message in response['Messages']:
                    # extract the message attributes you want to use as variables
                    order = message['MessageAttributes']['order']['StringValue']
                    word = message['MessageAttributes']['word']['StringValue']
                    handle = message['ReceiptHandle']

                    # store
                    messages.append({'order': order, 'word': word, 'handle': handle})

                # delete
                for msg in messages:
                    delete_message(msg['handle'])

                
                phrase = ' '.join([msg['word'] for msg in sorted(messages, key=lambda x: int(x['order']))])
            

            # If there are no messages in the queue, break the loop
            else:
                print("No messages in the queue")
                break
            
    # Handle any errors that may occur connecting to SQS
    except ClientError as e:
        print(e.response['Error']['Message'])
    
    return phrase  

# Trigger the function
if __name__ == "__main__":
    assembled_phrase = process_messages()  
    print("Assembled phrase:", assembled_phrase)  

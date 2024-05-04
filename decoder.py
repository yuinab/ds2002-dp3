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

def get_messages():
    try:
        # Receive messages from SQS queue
        response = sqs.receive_message(
            QueueUrl=url,
            AttributeNames=['All'],
            MaxNumberOfMessages=10,
            MessageAttributeNames=['All']
        )

        # Check if there are messages in the response
        if 'Messages' in response:
            messages = response['Messages']
            print(f"Received {len(messages)} messages:")
            word_pairs = []  # List to store word pairs
            for message in messages:
                # Extract message attributes
                order = int(message['MessageAttributes']['order']['StringValue'])
                word = message['MessageAttributes']['word']['StringValue']

                # Print message attributes
                print(f"Order: {order}, Word: {word}")

                # Append the word pair to the list
                word_pairs.append((order, word))

            # Sort the word pairs based on the order
            sorted_word_pairs = sorted(word_pairs, key=lambda x: x[0])
            print("Sorted Word Pairs:")
            for order, word in sorted_word_pairs:
                print(f"Order: {order}, Word: {word}")

            # delete
            for message in messages:
                delete_message(message['ReceiptHandle'])

        else:
            print("No messages received from the queue.")
    except ClientError as e:
        print("Error receiving messages:", e)

# Trigger the function
if __name__ == "__main__":
    get_messages()

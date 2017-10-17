import boto3
from . import TestTask


class QueManager:
    def __init__(self):
        self.sqs = boto3.client('sqs')
        self.task_queue_url = 'https://sqs.eu-central-1.amazonaws.com/838105386995/TestTasks'
        self.result_queue_url = 'https://sqs.eu-central-1.amazonaws.com/838105386995/TestResults'

    def get_task(self):
        response = self.sqs.receive_message(
            QueueUrl=self.task_queue_url,
            MessageAttributeNames=[
                'All'
            ]
        )

        if 'Messages' not in response:
            return None

        messages = response['Messages']

        if len(messages) > 0:
            print("we got a task")
            message = messages[0]

            self.sqs.delete_message(
                QueueUrl=self.task_queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )

            attribs = message['MessageAttributes']

            return TestTask(message['Body'], attribs['TestID']['StringValue'])

        return None

    def send_result(self, result, testid):
        self.sqs.send_message(
            QueueUrl=self.result_queue_url,
            MessageBody=result,
            MessageAttributes={
                'TestID': {
                    'StringValue': testid,
                    'DataType': 'String'
                }
            }
        )

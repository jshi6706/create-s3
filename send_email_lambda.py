import json
import smtplib
import os
import boto3

from email.mime.multipart import MIMEMutipart
from email.mime.text import MIMEText

smtp_server='smtp.gmail.com'
smtp_port=465
smtp_username='sjw292880@gmail.com'
smtp_password=""
send_to='jingwen.shi@sjsu.edu'
send_from="sjw292880@gmail.com"
message_sent='HELLO WORLD'

def send_email(msg):
    print('This is from smtplib')
    server=smtplib.SMTP_SSL(smtp_server,smtp_port)
    server.login(smtp_username,smtp_password)
    message= f"""From: {send_from}
To:{send_to}
Subject: Test message

{msg}."""
    server.sendmail(send_from,send_to,message)
    server.quit()


def smtp_send_email(res,acc,reg,db,tb,ch):
    send_to='jingwen.shi@sjsu.edu'
    send_from="sjw292880@gmail.com"

    
    msg = MIMEMutipart("alternative")
    msg=['From'] =send_from
    msg['To'] = send_to
    msg['Subject'] ='Schema CHnage Detect'

    html="""\
    <html>
      <head></head>
      <body>
            <h1>Schema Change Detected</h1><br>
            <br>
            Resource is:{resources}<br><br>
            Account is:{account}<br><br>
            Reigon is:{region}<br><br>
            Database Name is:{databaseName}<br><br>
            Table Name is{tableName}<br><br>
            Change is:{change}<br><br>
        </p>
      </body>
    </html>
    """.format(resources=res,account=acc,region=reg,databaseName=db,tableName=tb,change=ch)


    part2=MIMEText(html,'html')
    msg.attach(part2)

    #send message via local smtp server
    smtp_server='smtp.gmail.com'
    smtp_port=465
    smtp_username='sjw292880@gmail.com'
    smtp_password=""

    server.sendmail(send_from,send_to,msg.as_string())
    server.quit()

def send_to_sns(msg):
    client=boto3.client('sns')
    snsArn=''

    response=client.publish(
        TopicArn=snsArn,
        Messasge=msg,
        Subject='Schema Change Detect'

    )


def lambda_handler(event,context):
    print(f'event:{event}')
    for record in event['Records']:
        body=Record['body']
        deser_body=json.loads(body)
        message=deser_body['Message']
        deser_message=json.loads(message)
        resources=deser_message['resources'][0]
        account=deser_message['account']
        region=deser_message['account']
        detail=deser_message['detail']
        databaseName=deser_message['detail']['databaseName']
        tableName=deser_message['detail']['tableName']
        change=deser_message['detial']['typeOfChange']


        smtp_send_email(resources,account,region,databaseName,tableName,change)
        send_to_sns(change)
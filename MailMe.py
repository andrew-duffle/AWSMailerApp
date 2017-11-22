import psycopg2
import boto3
from botocore.client import Config
import smtplib
from mailer import Mailer
from mailer import Message
import time
import csv
import sys

timestr = time.strftime("%Y%m%d-%H%M%S")

def getdata():
	con=psycopg2.connect("dbname=DBName host=Host path get from console port=5439 user=User Name password=Your Password")
	cur = con.cursor()
	cur.execute("""
Enter a standard SQL query
	""")
	rows = cur.fetchall()
	fp = open('/tmp/'+'Your File Name',w') #<-You have to use tmp when dealing with lambda and S3
	myFile = csv.writer(fp)
	myFile.writerow(["Date"])
	myFile.writerows(rows)
	fp.close()
	con.close()
	print("Done")


def save():
	ACCESS_KEY_ID = 'S3 Access Key get from your console'
	ACCESS_SECRET_KEY = 'S3 secret key get from console. You can only get it one time so save it. You can create multiple'
	BUCKET_NAME = 'Your Bucket Name'
	data = open('/tmp/'+'Your File Name','rb')

	s3 = boto3.resource(
		's3',
		aws_access_key_id = ACCESS_KEY_ID,
		aws_secret_access_key = ACCESS_SECRET_KEY,
		config = Config(signature_version='s3v4')
		)
	s3.Bucket(BUCKET_NAME).put_object(Key='%sFileName' % timestr, Body=data)


def send():
	FROM = 'From Email Address'
	PW = 'Your Password'
	TO = 'Who you are sending it to'
	SUBJECT = 'The Subject Line'
	TEXT = 'Find this file at: Copy you S3 address here'
	mail = smtplib.SMTP('smtp.gmail.com',587) #<- the smtp will change based on what service you are using. Gmail is simple
	mail.ehlo()
	mail.starttls()
	mail.login(FROM,PW)

	BODY = '\r\n'.join(['To: %s' % TO,
			'From: %s' % FROM,
			'Subject: %s' % SUBJECT,
			'',TEXT])
	mail.sendmail(FROM,[TO],BODY)
	mail.close()

def GetSaveSend(event, context): #<-your lambda handeler 
	getdata()
	save()
	send()

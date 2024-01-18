import smtplib

import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup

def getHeadLines():
    url='https://www.bbc.com/news'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find('body').find_all('h3')
    print(headlines)
    finallist =""
    for head in headlines:
        finallist +=head.text.strip() +"\n"
    return finallist

def send_email(subject, body, smtp_server, smtp_port, mine_email, mine_password):
    message = MIMEMultipart()
    #set the required keys
    message['From'] = mine_email 
    message['To'] = mine_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(mine_email, mine_password)
            server.sendmail(mine_email, mine_email, message.as_string()) #send the email
    except smtplib.SMTPException as e:
        print(f"Failed to send email. Error: {e}")

def body_construct():
    fullbody = "" #This is just to have a value on initialise, this gets changed in the following lines
    try:
        file = open("body.txt","r")
        fullbody += file.read()
        fullbody += getHeadLines()
    except Exception as e:
        print(e)
     
    return fullbody
        
def daily_report():
    try:
        to_email = "poshie0456@gmail.com" #Change me
        smtp_server = "smtp.gmail.com" #Don't change unless it is needed (check your smtp server address)
        smtp_port = 465
        my_email = "poshie0456@gmail.com" #Change me
        my_password = "gcdl twrx xsun tuth"  #Please note, if you have 2fa, you need to setup a specific password, google how to depending on what email service you are using

        my_username = my_email.split('@')[0]
        subject = "Daily Email"
        body = f"Here is your daily email,  {my_username}:\n{datetime.date.today().strftime('%Y-%m-%d')}\n\n{body_construct()}" #add our constructed message to the body variable to be sent

        send_email(subject, body, smtp_server, smtp_port, my_email, my_password)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")




daily_report()
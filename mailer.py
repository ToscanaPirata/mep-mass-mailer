#!/usr/bin/env python3

from pprint import pprint
import csv
import re
import sys
import getopt
import smtplib
import time
from email.utils import formatdate
from email.utils import make_msgid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randint

lettera_plain = open("lettera.txt", encoding="utf-8").read()

sender_user = "[GMAIL USERNAME]" # CHANGEME <-- NOME UTENTE
sender_pwd = "[GmAIL PASSWORD]"; # CHANGEME <-- PASSWORD

mail_subject = "Protect Assange and the freedom of the press: support amendment 44!";

with open('it_meps.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file,delimiter=";")
    line_count = 0
    for row in csv_reader:
        print('[#] Sending to \t'+row["nome"]+' '+row["cognome"]+' '+row["mail"]+"\n")

        msg = MIMEMultipart("alternative")
        msg.set_charset("utf-8")

        subject = re.sub(r'{nome}', row["nome"], mail_subject)
        subject = re.sub(r'{cognome}', row["cognome"], subject)

        msg["Subject"] = subject
        msg["From"] = "" # CHANGEME <-- INSERIRE IL MITTENTE Nome Cognome <nome.cognome@gmail.com>
        msg["To"] = row["mail"]
        msg["Date"] = formatdate(localtime=True)

        message = re.sub(r'{nome}', row["nome"], lettera_plain)
        message = re.sub(r'{cognome}', row["cognome"], message)
        message = re.sub(r'{email}', row["mail"], message)

        part1 = MIMEText(message, "plain")
        msg.attach(part1)

        if(len(msg["To"]) > 0):
            try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.ehlo()
                server.login(sender_user, sender_pwd)
                server.sendmail(sender_user, msg["To"], msg.as_string())
                server.close()

                print("[#] Successfully sent email to "+msg["To"])
                time.sleep(5+randint(1, 20))
            except smtplib.SMTPException as e:
                print("[!] Unable to send email to "+msg["To"]+": "+str(e))


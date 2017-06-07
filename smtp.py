import sys
import imaplib
import getpass
import email
import email.header
import datetime
import time
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
from configparser import ConfigParser
from classes import *

# from pygeocoder import Geocoder
# import pandas as pd
# import numpy as np
# Geocoder.geocode("Benson Earth Sciences, 2200 Colorado Ave, Boulder, CO 80309").valid_address

config = ConfigParser()
config.read("config.ini")
EMAIL_ACCOUNT = config['Main']['Email']
PASSWORD = config['Main']['Password']

# Use 'INBOX' to read inbox.  Note that whatever folder is specified,
# after successfully running this script all emails in that folder
# will be marked as read.
EMAIL_FOLDER = "INBOX"


def process_mailbox(M):
    i=0
    global emailArray
    emailArray = []
    """
    Do something with emails messages in the folder.
    For the sake of this example, print some headers.
    """

    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print("No messages found!")
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])
        hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
        # Body (Payload) can be returned from get_payload as either a list of size 2 (1 = plain, 2 = html version(I THINK)) or a string
        try:
            body_plain_text = msg.get_payload(0)
            body = (str(body_plain_text))
        except:
            try:
                body = msg.get_payload()
            except:
                print("IDK")
                continue
        sender = msg.get_all("From")
        subject = str(hdr)
        # print('Message %s: %s' % (num, subject))
        # print('Raw Date:', msg['Date'])

        # Now convert to local date-time
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            # print ("Local Date:",local_date.strftime("%a, %d %b %Y %H:%M:%S"))

        # hdr_bdy = email.header.make_header(email.header.decode_header(msg['Body']))
    #    full_email = email.message_from_string(data[0][1]) # raw_email)

        # if msg.is_multipart():
        #     for part in msg.walk():
        #         ctype = part.get_content_type()
        #         cdispo = str(part.get('Content-Disposition'))
        #
        #         # skip any text/plain (txt) attachments
        #         if ctype == 'text/plain' and 'attachment' not in cdispo:
        #             body = part.get_payload(decode=True)  # decode
        #             break
        #  #   body = get_text(msg.get_payload(0))
        # # not multipart - i.e. plain text, no attachments, keeping fingers crossed
        # else:
        #     body = msg.get_payload(None, True) # body = bdy.get_payload(decode=True)


            ########################## FIND KEYWORDS ###############################


        if "free food" in str(body).lower():
            time = local_date.strftime("%a, %d %b %Y %H:%M:%S")
            sender =  sender[0].split("<")[1][:-1]
            # print('Message %s: %s' % (num, subject))
            # print("Local Date:", local_date.strftime("%a, %d %b %Y %H:%M:%S"))
            # print("Sender = " + sender)
            # print(body)
            emailObject = parsedEmail(subject, sender, time, body)
            emailArray.append(emailObject)


        i = i+1
        if i == 200:
            print("Parsing Done")
            break


M = imaplib.IMAP4_SSL('imap.gmail.com')


def login(M):
    try:
        rv, data = M.login(EMAIL_ACCOUNT, PASSWORD)
        # rv, data = M.login(EMAIL_ACCOUNT, getpass.getpass())
    except imaplib.IMAP4.error:
       print ("LOGIN FAILED!!! ")
       sys.exit(1)
    return rv, data

def start_process():
    rv, data = login(M)
    print(rv, data)
    rv, mailboxes = M.list()
    if rv == 'OK':
        print("Mailboxes:")
        print(mailboxes)
    rv, data = M.select(EMAIL_FOLDER)
    if rv == 'OK':
        print("Processing mailbox...\n")
        process_mailbox(M)
        M.close()
    else:
        print("ERROR: Unable to open mailbox ", rv)
    initalEmailDisplay()
    M.logout()

def initalEmailDisplay():
    length = str(len(emailArray))
    emailLabel.config(text='1' + '/' + length)
    fillEmailFields()

def fillEmailFields():
    emailPosition = int(emailLabel.cget("text").split('/')[0]) - 1
    currentEmail = emailArray[emailPosition]
    subjectEntry.delete(0, END)
    fromEntry.delete(0, END)
    timeEntry.delete(0, END)
    bodyScrolledText.delete(1.0, END)
    subjectEntry.insert(0, currentEmail.subject)
    fromEntry.insert(0, currentEmail.sender)
    timeEntry.insert(0, currentEmail.time)
    bodyScrolledText.insert(1.0, currentEmail.body)

def nextEmail(number):
    emailLabelText = emailLabel.cget("text").split('/')
    currentEmailPosition = int(emailLabelText[0]) - 1
    totalEmails = int(emailLabelText[1])
    if totalEmails == 0:
        return
    else:
        nextEmailPosition = (currentEmailPosition + number) % totalEmails
        emailLabel.config(text=str(nextEmailPosition + 1) + '/' + str(totalEmails))
        fillEmailFields()

def doNothing():
    return

root = Tk()
root.title("Free Food")
# Menu Bar Creation
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)
# Creating Left and Right Boxes of ui
leftBox = Frame(root, borderwidth=0)
rightBox = Frame(root, borderwidth=5)

leftBox.pack(side=LEFT)
rightBox.pack(side=RIGHT)

#Creation of ui elements
# Left
subjectLabel = Label(leftBox, text='Subject')
subjectEntry = Entry(leftBox, width=100)

fromLabel = Label(leftBox, text='From')
fromEntry = Entry(leftBox, width=100)

timeLabel = Label(leftBox, text='Time')
timeEntry = Entry(leftBox, width=100)

bodyLabel = Label(leftBox, text='Body')
bodyScrolledText = ScrolledText(leftBox, height=30, width=100, undo=True)
# Right
parseButton = Button(rightBox, text="Parse", width=25, command=lambda: start_process())

titleLabel = Label(rightBox, text='Title')
titleEntry = Entry(rightBox, width=50)

groupLabel = Label(rightBox, text='Group')
groupEntry = Entry(rightBox, width=50)

locationLabel = Label(rightBox, text='Location')
locationEntry = Entry(rightBox, width=50)

timeLabel = Label(rightBox, text='Time')
timeEntry = Entry(rightBox, width=50)

dateLabel = Label(rightBox, text='Date')
dateEntry = Entry(rightBox, width=50)

descriptionLabel = Label(rightBox, text='Subject')
descriptionScrolledText = ScrolledText(rightBox, height=20, width=50, undo=True)

emailLabel = Label(rightBox, text='0/0')
previousButton = Button(rightBox, text="<Prev", width=25, command=lambda: nextEmail(-1))
confirmButton = Button(rightBox, text="Confirm", width=25,background="red",  command=lambda: doNothing())
nextButton = Button(rightBox, text="Next>", width=25,  command=lambda: nextEmail(1))

#Adding ui elements
# Left
subjectLabel.grid(row=9)
subjectEntry.grid(row=9, column=1, padx=10, pady=2)

fromLabel.grid(row=10)
fromEntry.grid(row=10, column=1, padx=10, pady=2)

timeLabel.grid(row=11)
timeEntry.grid(row=11, column=1, padx=10, pady=2)

bodyLabel.grid(row=12)
bodyScrolledText.grid(row=12, column=1, padx=10, pady=10)
# Right
parseButton.grid(column=1, row = 7, pady = 2, columnspan=3)

titleLabel.grid(row=9)
titleEntry.grid(row=9, column=1, padx=10, pady=2,columnspan=3)

groupLabel.grid(row=10)
groupEntry.grid(row=10, column=1, padx=10, pady=2,columnspan=3)

locationLabel.grid(row=11)
locationEntry.grid(row=11, column=1, padx=10, pady=2,columnspan=3)

timeLabel.grid(row=13)
timeEntry.grid(row=13, column=1, padx=10, pady=2,columnspan=3)

dateLabel.grid(row=12, column=0)
dateEntry.grid(row=12, column=1, padx=10, pady=2,columnspan=3)

descriptionLabel.grid(row=14)
descriptionScrolledText.grid(row=14, column=1, padx=10, pady=10,columnspan=3)

emailLabel.grid(row=20, column=2)
previousButton.grid(column=1, row = 20, pady = 10, sticky=W)
confirmButton.grid(column=2, row = 21, pady = 10)
nextButton.grid(column=3, row = 20, pady = 10, sticky=E)

root.mainloop()
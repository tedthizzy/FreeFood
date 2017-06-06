import sys
import imaplib
import getpass
import email
import email.header
import datetime
import time
from configparser import ConfigParser

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
            print(str(body_plain_text))
        except:
            try:
                body_plain_text = msg.get_payload()
            except:
                print("IDK")
                continue

        subject = str(hdr)
        print('Message %s: %s' % (num, subject))
        # print('Raw Date:', msg['Date'])

        # Now convert to local date-time
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            print ("Local Date:", \
                local_date.strftime("%a, %d %b %Y %H:%M:%S"))

        # hdr_bdy = email.header.make_header(email.header.decode_header(msg['Body']))
    #    full_email = email.message_from_string(data[0][1]) # raw_email)
        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))

                # skip any text/plain (txt) attachments
                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    body = part.get_payload(decode=True)  # decode
                    break
         #   body = get_text(msg.get_payload(0))
        # not multipart - i.e. plain text, no attachments, keeping fingers crossed
        else:
            body = msg.get_payload(None, True) # body = bdy.get_payload(decode=True)


            ########################## FIND KEYWORDS ###############################


        if "food" in str(body).lower():
            if "public" in str(body).lower():
                print(body)
                time.sleep(4)

        i = i+1
        if i == 10:
            break




M = imaplib.IMAP4_SSL('imap.gmail.com')

try:
    rv, data = M.login(EMAIL_ACCOUNT, PASSWORD)
    # rv, data = M.login(EMAIL_ACCOUNT, getpass.getpass())

except imaplib.IMAP4.error:
   print ("LOGIN FAILED!!! ")
   sys.exit(1)

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
M.logout()
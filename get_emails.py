import imaplib
from time import sleep
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")
EMAIL_ACCOUNT = config['Main']['Email']
PASSWORD = config['Main']['Password']

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(EMAIL_ACCOUNT, PASSWORD)
mail.list()
# Out: list of "folders" aka labels in gmail.
mail.select("inbox") # connect to inbox.

result, data = mail.search(None, "ALL")

ids = data[0] # data is a list.
id_list = ids.split() # ids is a space separated string
latest_email_id = id_list[-1] # get the latest

result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID

raw_email = str(data[0][1])
# print(raw_email)

##########################################################################################

import email
a = raw_email

b = email.message_from_string(a)
body = ""

if b.is_multipart():
    for part in b.walk():
        ctype = part.get_content_type()
        cdispo = str(part.get('Content-Disposition'))

        # skip any text/plain (txt) attachments
        if ctype == 'text/plain' and 'attachment' not in cdispo:
            body = part.get_payload(decode=True)  # decode
            break
# not multipart - i.e. plain text, no attachments, keeping fingers crossed
else:
    body = b.get_payload(decode=True)


print("print the body:")
print(body)

##########################################################################################

import imapclient
imapObj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
imapObj.login(' theo4629@gmail.com ', ' !nt0th3w00dz ') imapObj.select_folder('INBOX', readonly=True)
UIDs = imapObj.search(['SINCE 05-Jul-2014'])
UIDs
rawMessages = imapObj.fetch([40041], ['BODY[]', 'FLAGS'])

##########################################################################################

import pyzmail
message = pyzmail.PyzMessage.factory(rawMessages[40041]['BODY[]'])
message.get_subject()
message.get_addresses('from')
message.get_addresses('to')
message.get_addresses('cc')
message.get_addresses('bcc')
message.text_part != None
message.text_part.get_payload().decode(message.text_part.charset)
message.html_part != None
message.html_part.get_payload().decode(message.html_part.charset)
imapObj.logout()




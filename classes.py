class parsedEmail():
    def __init__(self,uid, subject, sender, senderName, time, body):
        self.uid = uid
        self.subject = subject
        self.sender = sender
        self.senderName = senderName
        self.time = time
        self.body = body

        self.title = ""
        self.group = ""
        self.location = ""
        self.date = ""
        # self.time = ""
        # Need to find other name
        self.details = ""

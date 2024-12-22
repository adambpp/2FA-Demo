import secrets as s
import smtplib, ssl

class CodeGenerator:

    # constructor
    def __init__(self):
        pass

    '''
    This method generates a one time password (no timer, that will be in a different class)
    
    parameters: nothing
    
    returns: the generated one time password
    '''
    def generate_code(self):
        return "".join(str(s.randbelow(9)) for i in range(0, 6))



# testing email stuff
port = 465 # for SSL
smtp_server = "smtp.gmail.com"
sender_email = ""
receiver_email = ""
password = ""
message = """\
Subject: Hi there

This message is sent from Python
"""

# create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
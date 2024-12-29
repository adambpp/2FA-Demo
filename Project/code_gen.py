import secrets as s
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

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


class EmailOTP:
    def __init__(self):
        self.__otp = None


    def __generate_otp(self): # double underscore to indicate that this method is private
        self.__otp = CodeGenerator().generate_code()
        return self.__otp

    def get_otp(self):
        return self.__otp


    def generate_email(self, receiver_email, password):
        # variables to easily change values
        otp = self.__generate_otp()
        sender_email = ""

        message = MIMEMultipart("alternative")
        message["Subject"] = "multipart test"
        message["From"] = sender_email
        message["To"] = receiver_email

        text = f"""\
        Hi,
        Below is your 6-digit code you need to sign in:
        {otp}"""

        html = f"""  
         <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.5; color: #333; margin: 0; padding: 0">
              <table align="center" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; background-color: #ffffff;">
                <tr>
                  <td style="padding: 10px; text-align: left;">
                    <p align="center" style="margin: 0; font-size: 16px; color: #333;">
                       Hi,<br><br>
                       Below is your 6-digit code you need to sign in:<br><br>
                    </p>
                    <div align="center" style="margin: 0 auto; max-width: 300px; border-radius: 15px; background-color: lightgrey; padding: 10px; padding-bottom: 0;">
                        <strong style="letter-spacing: 10px; font-size: 50px; color: #000;">{otp}</strong><br><br>
                    </div>
                    <p align="center">This code is valid for <strong>60 seconds</strong></p>
                  </td>
                </tr>
              </table>
            </body>
          </html>
        """

        # turn the messages into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # add HTML/plain-test parts to MIMEMultipart message
        # email client tries to render the last part (html) first
        message.attach(part1)
        message.attach(part2)

        # create a secure connection with server and send email
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
        except Exception as e:
            return -1

class AccountStorage:
    def __init__(self):
        self.generator = EmailOTP()
        self.accounts = []
        self.start_time = None
        self.end_time = None

    def add_account(self, email, password):
        self.accounts.append({"email": email, "password": password})
        print(self.accounts)

    def get_email(self, email):
        return self.accounts[email]["email"]

    def get_password(self, email):
        return self.accounts[email]["password"]

    def send_otp_code(self, email, password):
        if self.generator.generate_email(email, password) == -1:
            return -1
        self.start_time = time.time()

    def verify_otp_code(self, inputted_code):
        self.end_time = time.time()
        time_diff = self.end_time - self.start_time
        if time_diff < 60 and inputted_code == self.generator.get_otp():
            return True
        else:
            return False




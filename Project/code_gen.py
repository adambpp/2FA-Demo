import secrets
import secrets as s
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time as t

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


    def generate_otp(self):
        self.__otp = CodeGenerator().generate_code()
        return self.__otp

    def get_otp(self):
        return self.__otp


    def generate_email(self, receiver_email, password):
        # variables to easily change values
        otp = self.generate_otp()
        sender_email = ""

        message = MIMEMultipart("alternative")
        message["Subject"] = "multipart test"
        message["From"] = sender_email
        message["To"] = receiver_email

        text = """\
        Hi,
        How are you?
        Real Python has many great tutorials:
        www.realpython.com"""

        # this is random chatgpt html, replace later with html that I made myself
        html = f"""  
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.5; color: #333; margin: 0; padding: 0;">
            <table align="center" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; background-color: #ffffff;">
              <tr>
                <td style="padding: 10px; text-align: left;">
                  <p style="margin: 0; font-size: 16px; color: #333;">
                     Hi,<br><br>
                     How are you?<br><br>
                     Your OTP is: <strong style="font-size: 18px; color: #000;">{otp}</strong><br><br>
                  </p>
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
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())




# testing basic application functionality
email_otp = EmailOTP()
user_email = str(input("Enter your email: "))
start_time = t.time()
email_otp.generate_email(user_email)
user_otp = str(input("Enter your OTP that was sent to your email: "))
end_time = t.time()
print(end_time - start_time)
if email_otp.get_otp() == user_otp and end_time - start_time < 30:
    print("entry confirmed, welcome!")


import secrets as s
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

'''
The sole purpose of this class is just to generate the code to be used in the email. This class only have one method
is prob useless and could just be put into the EmailOTP class, but I will leave it like this for now.
'''
class CodeGenerator:

    # constructor
    def __init__(self):
        pass

    '''
    This method generates a 6-digit one time password with more secure randomness via the secrets library
        
    returns: the generated one time password
    '''
    def generate_code(self):
        return "".join(str(s.randbelow(9)) for i in range(0, 6))


'''
This purpose of this class is to actually send out the email
'''
class EmailOTP:
    # constructor
    def __init__(self):
        self.__otp = None


    '''
    Generates a 6-digit one time password via the CodeGenerator class
    
    returns: the generated one time password
    '''
    def __generate_otp(self): # double underscore to indicate that this method is private
        self.__otp = CodeGenerator().generate_code()
        return self.__otp

    '''
    Obtain the generated one time password
    '''
    def get_otp(self):
        return self.__otp


    '''
    Send out an email to the given recipient. The email includes both plain text and HTML formats
    for compatibility with different email clients. Ensure the sender email is configured to allow secure access.
    The OTP that is sent out will be valid for 60 seconds.
    
    Parameters:
        receiver_email: the email to send the message to
        password: the password to the email account to send the message to
        
    returns:
        -1 if the email sending was unsuccessful, nothing otherwise
    '''
    def generate_email(self, receiver_email, password):
        otp = self.__generate_otp()
        # fill this in with the email you want to use as the sender email
        sender_email = ""

        message = MIMEMultipart("alternative")
        message["Subject"] = "Login Verification Code"
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
            # return -1 if the email was not successfully sent
            return -1


'''
This class stores the account(s) that the user makes via an email and password. In a real word this should use
hashing to securely store the users information (I might even add this later) but for now I just add them to a 
dictionary since this is not a real world application
'''
class AccountStorage:
    # CONSTRUCTOR
    def __init__(self):
        self.generator = EmailOTP()
        self.accounts = []
        self.start_time = None
        self.end_time = None

    '''
    Adds a new account (email, password) to the database
    '''
    def add_account(self, email, password):
        self.accounts.append({"email": email, "password": password})

    '''
    Get a certain email from the database
    
    Parameters:
        email: the email to obtain
    '''
    def get_email(self, email):
        return self.accounts[email]["email"]

    '''
    Get a certain password from the database

    Parameters:
        email: the password to obtain
    '''
    def get_password(self, email):
        return self.accounts[email]["password"]

    '''
    Sends a 6-digit one time login code to the users email. Also store the current 
    
    Parameters:
        email: the email of the user
        password: the password of the user
    
    Returns:
        -1 if the email sending was unsuccessful, nothing otherwise
    '''
    def send_otp_code(self, email, password):
        if self.generator.generate_email(email, password) == -1:
            return -1
        self.start_time = time.time()

    '''
    Verifies the the code that the user entered, seeing if it matches the code that was sent to the email
    
    Parameters:
        inputted_code: the code inputted by the user
    '''
    def verify_otp_code(self, inputted_code):
        self.end_time = time.time()
        time_diff = self.end_time - self.start_time
        if time_diff < 60 and inputted_code == self.generator.get_otp():
            return True
        else:
            return False




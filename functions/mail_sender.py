
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import dns.resolver
from email.mime.base import MIMEBase
from email import encoders


# Email configuration
import re



    
class sender:
    def __init__(self,emailPass):
        self.Admin = "maged.khaled03@gmail.com"
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587  # or the appropriate port for your SMTP server
        self.sender_email = 'Medad.WS@gmail.com'
        self.sender_password = emailPass
        self.receiver_email = ""
        self.subject = ""
        self.message = ""
    
    def send(self,data):
        
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = data['To']
        msg['Subject'] = data['title']
        
            
            

        # Add the message to the body of the email
        msg.attach(MIMEText(data['message'], 'plain'))
        text = msg.as_string()
        if data['attachment'] :
            with open(data['attachment'], "rb") as attachment:
                # Create a base object and set the appropriate MIME type
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
            # Encode the attachment in Base64
            encoders.encode_base64(part)
            
            # Add headers to the attachment
            
            filename = data['attachment'].split('/')
            name = filename[-1]
            
            part.add_header(
                "Content-Disposition",
                "attachment; filename= " + name)
            
            
            # Attach the attachment to the email message
            msg.attach(part)
            
            # Convert the message to a string
            text = msg.as_string()

        # Create a secure connection to the SMTP server
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            # Login to the sender's email account
            server.login(self.sender_email, self.sender_password)
            # Send the email
            server.sendmail(self.sender_email, data['To'], text)
            
            print('Email sent successfully!')
        
        
        

    def valide_email(self,email):
        # Syntax check
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            return False
    
        local_part, domain = email.split('@')

        # Perform MX record lookup
        try:
            answers = dns.resolver.query(domain, 'MX')
            return True
        except :
            return False

        return False

        



        
        
        


        
        
        
        
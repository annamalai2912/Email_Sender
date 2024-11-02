import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def validate_sender_email(sender_email, password):
    """
    Validate the sender's email and password by attempting to log in to the SMTP server.
    This function doesn't send an email but checks if the credentials are correct.
    """
    try:
        # Create a connection to the SMTP server (using Gmail as an example)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Start TLS for security
        server.login(sender_email, password)  # Log in to the server
        server.quit()  # Log out
        return True  # Valid credentials
    except smtplib.SMTPAuthenticationError:
        return False  # Invalid credentials
    except Exception as e:
        print(f"An error occurred during authentication: {e}")
        return False

def send_email(sender_email, password, recipient_email, subject, body, attachments=None):
    """
    Send an email with the specified subject, body, and attachments.
    """
    try:
        # Validate recipient email
        if not is_valid_email(recipient_email):
            raise ValueError(f"Invalid recipient email: {recipient_email}")

        # Set up the email server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, password)  # Log in to the server

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Add attachments if any
        if attachments:
            for file in attachments:
                if os.path.isfile(file):
                    with open(file, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file)}"')
                        msg.attach(part)
                else:
                    print(f"File not found: {file}")

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()  # Log out
        print(f"Email sent to {recipient_email}")
        return True  # Indicate success
    except Exception as e:
        print(f"Failed to send email to {recipient_email}. Error: {e}")
        return False  # Indicate failure


def is_valid_email(email):
    """
    Check if the provided email is valid using regex.
    """
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email) is not None

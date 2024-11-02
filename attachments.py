import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def attach_file(msg: MIMEMultipart, file_path: str):
    """Attach a file to the email message."""
    if os.path.isfile(file_path):
        try:
            with open(file_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
                msg.attach(part)
        except Exception as e:
            print(f"Error attaching file {file_path}: {e}")
    else:
        print(f"The file {file_path} does not exist.")

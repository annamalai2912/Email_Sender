import csv
from email_sender import send_email

def send_bulk_emails(csv_file, sender_email, sender_password, subject, body, attachment_paths):
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            recipient = row['email_address']  # Ensure your CSV has this column
            try:
                send_email(sender_email, sender_password, recipient, subject, body, attachment_paths)
                # Optionally log the email sending here
            except Exception as e:
                print(f"Failed to send email to {recipient}: {str(e)}")

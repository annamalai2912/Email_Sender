import datetime

LOG_FILE = 'email_history.log'

def log_email(sender, recipient, subject):
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"{datetime.datetime.now()}: Sent email from {sender} to {recipient} with subject: '{subject}'\n")
import csv

# Placeholder for email log storage; ideally, this should be a persistent storage solution
email_history = []

def log_email(sender, recipient, subject):
    email_history.append({'sender': sender, 'recipient': recipient, 'subject': subject})

def save_email_history_to_csv(file_path):
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['sender', 'recipient', 'subject']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for email in email_history:
            writer.writerow(email)

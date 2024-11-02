import threading
import os
import time
import json
from datetime import datetime
from email_sender import send_email

class EmailScheduler:
    def __init__(self, storage_file="scheduled_emails.json"):
        self.storage_file = storage_file
        self.scheduled_emails = self.load_scheduled_emails()
        self.running = True
        self.check_interval = 60  # Check every 60 seconds

        # Start the scheduler in a separate thread
        threading.Thread(target=self.run_scheduler, daemon=True).start()

    def load_scheduled_emails(self):
        """
        Load scheduled emails from a JSON file.
        """
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as file:
                return json.load(file)
        return []

    def save_scheduled_emails(self):
        """
        Save scheduled emails to a JSON file.
        """
        with open(self.storage_file, "w") as file:
            json.dump(self.scheduled_emails, file, default=str)

    def schedule_email(self, sender, password, recipient, subject, body, attachments, send_time):
        """
        Schedule an email by adding it to the list and saving it.
        """
        send_time = datetime.strptime(send_time, "%Y-%m-%d %H:%M:%S")

        self.scheduled_emails.append({
            'sender': sender,
            'password': password,
            'recipient': recipient,
            'subject': subject,
            'body': body,
            'attachments': attachments,
            'send_time': send_time
        })
        self.save_scheduled_emails()
        print(f"[{datetime.now()}] Scheduled email to {recipient} at {send_time}.")

    def run_scheduler(self):
        """
        Continuously checks and sends emails due to be sent.
        """
        while self.running:
            now = datetime.now()
            for email_info in self.scheduled_emails[:]:
                send_time = datetime.strptime(email_info['send_time'], "%Y-%m-%d %H:%M:%S")
                if send_time <= now:
                    self.send_scheduled_email(email_info)
                    self.scheduled_emails.remove(email_info)  # Remove after sending
                    self.save_scheduled_emails()
            time.sleep(self.check_interval)  # Check every minute

    def send_scheduled_email(self, email_info):
        """
        Send the email and handle errors.
        """
        try:
            send_email(email_info['sender'], email_info['password'], email_info['recipient'],
                       email_info['subject'], email_info['body'], email_info['attachments'])
            print(f"[{datetime.now()}] Email sent to {email_info['recipient']} successfully.")
        except Exception as e:
            print(f"[{datetime.now()}] Failed to send email to {email_info['recipient']}. Error: {e}")

# Usage example:
# email_scheduler = EmailScheduler()
# email_scheduler.schedule_email("sender@example.com", "password", "recipient@example.com", 
#                                "Subject", "Body text", ["file1.pdf"], "2024-11-02 17:30")

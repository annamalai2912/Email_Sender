import sys
import os
import re
import json
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QLabel,
    QProgressBar,
    QInputDialog,
    QComboBox,
)
from email_sender import send_email, validate_sender_email
from templates import EmailTemplateManager
from bulk_sender import send_bulk_emails
from history import log_email, save_email_history_to_csv
from contact_importer import import_contacts
from scheduler import EmailScheduler

class EmailSenderWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.template_manager = EmailTemplateManager()
        self.email_scheduler = EmailScheduler()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Email form
        form_layout = QFormLayout()
        self.sender_email = QLineEdit()
        self.sender_password = QLineEdit()
        self.recipient_email = QLineEdit()
        self.subject = QLineEdit()
        self.body_text = QTextEdit()
        self.attachment_paths = []
        self.recent_recipients = []

        # Set password input to hide characters
        self.sender_password.setEchoMode(QLineEdit.Password)

        form_layout.addRow("Sender Email:", self.sender_email)
        form_layout.addRow("Sender Password:", self.sender_password)
        form_layout.addRow("Recipient Email:", self.recipient_email)
        form_layout.addRow("Subject:", self.subject)
        form_layout.addRow("Body:", self.body_text)

        # Attachments button
        self.attach_button = QPushButton("Attach Files")
        self.attach_button.clicked.connect(self.attach_files)

        # Send Email Button
        send_button = QPushButton("Send Email")
        send_button.clicked.connect(self.send_email)

        # Bulk Send Button
        self.bulk_send_button = QPushButton("Browse for Bulk Email CSV")
        self.bulk_send_button.clicked.connect(self.browse_bulk_csv)

        # Schedule Email Button (not implemented)
        schedule_button = QPushButton("Schedule Email")
        schedule_button.clicked.connect(self.schedule_email)

        # Import Contacts Button
        import_button = QPushButton("Import Contacts")
        import_button.clicked.connect(self.import_contacts)

        # Export History Button
        export_history_button = QPushButton("Export Email History to CSV")
        export_history_button.clicked.connect(self.export_email_history)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        self.sender_email = QComboBox()
        self.load_recent_recipients()  # Load recent emails into the combo box
        self.sender_email.setEditable(True)

        form_layout.addRow("Sender Email:", self.sender_email)  

        layout.addLayout(form_layout)
        layout.addWidget(self.attach_button)
        layout.addWidget(send_button)
        layout.addWidget(self.bulk_send_button)
        layout.addWidget(schedule_button)
        layout.addWidget(import_button)
        layout.addWidget(export_history_button)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)
        self.setWindowTitle("Email Sender")
        self.resize(400, 600)

    def attach_files(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", "All Files (*)", options=options)
        if files:
            self.attachment_paths.extend(files)
            QMessageBox.information(self, "Files Attached", f"Attached: {', '.join(os.path.basename(f) for f in files)}")
    def load_recent_recipients(self):
    #"""Load recent recipients from a JSON file into the combo box."""
        if os.path.exists('recent_recipients.json'):
            with open('recent_recipients.json', 'r') as file:
                self.recent_recipients = json.load(file)
                self.sender_email.addItems(self.recent_recipients)
        else:
            self.recent_recipients = []


    def send_email(self):
        sender = self.sender_email.currentText()
        password = self.sender_password.text()
        recipient = self.recipient_email.text()
        subject = self.subject.text()
        body = self.body_text.toPlainText()

        if not all([sender, password, recipient, subject, body]):
            QMessageBox.warning(self, "Input Error", "Please fill all fields before sending an email.")
            return

        # Validate sender email and password
        if not validate_sender_email(sender, password):
            QMessageBox.warning(self, "Validation Error", "Sender email or password is incorrect.")
            return

        # Validate recipient email
        if not self.is_valid_email(recipient):
            QMessageBox.warning(self, "Validation Error", "Recipient email is invalid.")
            return

        try:
            send_email(sender, password, recipient, subject, body, self.attachment_paths)
            log_email(sender, recipient, subject)
            QMessageBox.information(self, "Success", "Email sent successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def browse_bulk_csv(self):
        sender = self.sender_email.text()
        password = self.sender_password.text()
        subject = self.subject.text()
        body = self.body_text.toPlainText()

        if not all([sender, password, subject, body]):
            QMessageBox.warning(self, "Input Error", "Please fill Sender Email, Password, Subject, and Body fields before bulk sending.")
            return

        # Validate sender email and password
        if not validate_sender_email(sender, password):
            QMessageBox.warning(self, "Validation Error", "Sender email or password is incorrect.")
            return

        options = QFileDialog.Options()
        csv_file, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if csv_file:
            self.progress_bar.setValue(0)
            try:
                total_recipients = self.get_recipient_count_from_csv(csv_file)
                if total_recipients == 0:
                    QMessageBox.warning(self, "No Recipients", "No valid recipients found in the CSV.")
                    return

                # Start the bulk email sending process
                self.progress_bar.setRange(0, total_recipients)
                for index in range(total_recipients):
                    recipient_email = self.get_recipient_email(csv_file, index)
                    if self.is_valid_email(recipient_email):
                        send_email(sender, password, recipient_email, subject, body, self.attachment_paths)
                        self.progress_bar.setValue(index + 1)
                    else:
                        QMessageBox.warning(self, "Invalid Recipient", f"Recipient email '{recipient_email}' is invalid. Skipping...")
                
                QMessageBox.information(self, "Success", "Bulk emails sent successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    
    def schedule_email(self):
        sender = self.sender_email.currentText()
        password = self.sender_password.text()
        recipient = self.recipient_email.text()
        subject = self.subject.text()
        body = self.body_text.toPlainText()

        if not all([sender, password, recipient, subject, body]):
            QMessageBox.warning(self, "Input Error", "Please fill all fields before scheduling an email.")
            return

        # Prompt the user to select date and time
        datetime_str, ok = QInputDialog.getText(self, "Schedule Email", "Enter date and time (YYYY-MM-DD HH:MM):")
        
        if not ok or not datetime_str:
            QMessageBox.warning(self, "Input Error", "Please provide a valid date and time for scheduling.")
            return

        try:
            # Schedule the email using EmailScheduler
            self.email_scheduler.schedule_email(sender, password, recipient, subject, body, self.attachment_paths, datetime_str)
            QMessageBox.information(self, "Scheduled", "Email scheduled successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to schedule email: {e}")


    def import_contacts(self):
        options = QFileDialog.Options()
        csv_file, _ = QFileDialog.getOpenFileName(self, "Select Contacts CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if csv_file:
            try:
                contacts = import_contacts(csv_file)  # Pass the selected CSV file to the function
                if contacts:
                    QMessageBox.information(self, "Contacts Imported", f"Imported {len(contacts)} contacts.")
                else:
                    QMessageBox.warning(self, "No Contacts", "No contacts found in the CSV.")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def export_email_history(self):
        options = QFileDialog.Options()
        csv_file, _ = QFileDialog.getSaveFileName(self, "Save Email History as CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if csv_file:
            try:
                save_email_history_to_csv(csv_file)  
                QMessageBox.information(self, "Success", "Email history exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def is_valid_email(self, email):
        """ Validate email format. """
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_regex, email) is not None

    def get_recipient_count_from_csv(self, csv_file):
        """ Get the count of valid recipients from the CSV file. """
        count = 0
        with open(csv_file, 'r') as file:
            for line in file:
                recipient_email = line.strip().split(',')[0]  # Adjust based on your CSV structure
                if self.is_valid_email(recipient_email):
                    count += 1
        return count
    def add_recipient_to_history(self, recipient):
        """Add recipient to the history and save to JSON."""
        if recipient not in self.recent_recipients:
            self.recent_recipients.append(recipient)
            with open('recent_recipients.json', 'w') as file:
                json.dump(self.recent_recipients, file) 

    def get_recipient_email(self, csv_file, index):
        """ Get the recipient email from the CSV file based on index. """
        with open(csv_file, 'r') as file:
            for i, line in enumerate(file):
                if i == index:
                    return line.strip().split(',')[0]  # Adjust based on your CSV structure
        return None

def start_gui():
    app = QApplication(sys.argv)
    sender_widget = EmailSenderWidget()
    sender_widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    start_gui()

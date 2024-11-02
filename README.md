To create documentation for your project, I'll help you draft a `README.md` that describes each file's purpose, as well as instructions for setting up and using the project. Below is an example `README.md` that you can customize as needed. 

---

# Project Name

## Overview

This project is designed to facilitate bulk email sending with a scheduling feature. The application reads contact information, schedules emails, and provides a user interface for managing email templates and history. It's useful for anyone who needs to manage and send large quantities of emails regularly.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Configuration](#configuration)
- [License](#license)

## Features
- Bulk email sending with CSV-based contact management.
- Scheduling of emails to be sent at specified times.
- User-friendly interface for managing email templates and contacts.
- Tracking of recent recipients and email history.
- Customizable email templates.

## Requirements
Make sure you have the following installed:
- Python 3.x
- Required libraries (listed in `requirements.txt`)

Install the dependencies by running:
```bash
pip install -r requirements.txt
```

## Setup
1. Clone the repository to your local machine.
2. Install the required Python packages (see [Requirements](#requirements)).
3. Add your email credentials (SMTP server, username, password) to the appropriate configuration file if needed.

## Usage
To start the application, run:
```bash
python main.py
```

The main script initiates the user interface where you can upload contact files, select email templates, and schedule emails. 

## File Structure
Here's a breakdown of the main files in the project:

### Code Files
- **attachments.py**: Handles file attachments for emails.
- **bulk_sender.py**: Responsible for sending bulk emails.
- **contact_imponer.py**: Parses and imports contact data from `contacts.csv`.
- **contacts.csv**: Stores the contact information in CSV format.
- **email_sender.py**: Handles the core email sending functionality, including composing emails and sending individual messages.
- **history.py**: Manages email history records, allowing the user to review sent emails.
- **main.py**: Entry point of the application that initializes the UI and coordinates different components.
- **recent_recipients.json**: Keeps track of the most recent email recipients for quick access.
- **requirements.txt**: Contains a list of required Python packages for the project.
- **scheduled_emails.json**: Stores information about scheduled emails that are queued for future sending.
- **scheduler.py**: Manages scheduling logic for timed email sending.
- **templates.py**: Handles loading and editing email templates.
- **todays.csv**: Records contacts scheduled for emails today.
- **ui.py**: Manages the graphical user interface of the application, enabling user interaction.

### Configuration and Data Files
- **contacts.csv**: Holds the contact list in CSV format.
- **recent_recipients.json**: Stores the list of recent recipients.
- **scheduled_emails.json**: Tracks emails scheduled to be sent in the future.
- **todays.csv**: Contains the list of contacts to email on the current day.

## Configuration
Ensure you configure the SMTP settings in the appropriate place within `email_sender.py` or other specified files.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

You can copy this template into your `README.md` file, making modifications to better match your project's specifics. Let me know if you’d like additional details for any part!
import csv

def import_contacts(csv_file):
    contacts = []
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            contacts.append(row['email_address'])  # Ensure your CSV has this column
    return contacts

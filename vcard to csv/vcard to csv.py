import csv
import re
import os

def parse_vcard(vcard_file):
    """
    Parse a vCard (.vcf) file and extract contact details.
    
    Args:
        vcard_file (str): Path to the vCard file.

    Returns:
        list: A list of dictionaries containing contact information.
    """
    contacts = []
    
    with open(vcard_file, 'r', encoding='utf-8') as file:
        contact = {}
        for line in file:
            line = line.strip()

            # New contact starts
            if line == "BEGIN:VCARD":
                contact = {}

            # Contact ends
            elif line == "END:VCARD":
                if contact:
                    contacts.append(contact)

            # Extract name
            elif line.startswith("FN:"):
                contact['Full Name'] = line[3:]

            # Extract organization
            elif line.startswith("ORG:"):
                contact['Organization'] = line[4:]

            # Extract phone numbers
            elif line.startswith("TEL;") or line.startswith("TEL:"):
                phone = re.sub(r"^TEL(;.+)?:", "", line)
                if 'Phone Numbers' not in contact:
                    contact['Phone Numbers'] = []
                contact['Phone Numbers'].append(phone)

            # Extract email addresses
            elif line.startswith("EMAIL;") or line.startswith("EMAIL:"):
                email = re.sub(r"^EMAIL(;.+)?:", "", line)
                if 'Emails' not in contact:
                    contact['Emails'] = []
                contact['Emails'].append(email)

        # Normalize phone numbers and emails as single strings
        for contact in contacts:
            if 'Phone Numbers' in contact:
                contact['Phone Numbers'] = ", ".join(contact['Phone Numbers'])
            if 'Emails' in contact:
                contact['Emails'] = ", ".join(contact['Emails'])

    return contacts

def write_to_csv(contacts, output_file):
    """
    Write contact details to a CSV file.

    Args:
        contacts (list): A list of dictionaries containing contact information.
        output_file (str): Path to the output CSV file.
    """
    if not contacts:
        print("No contacts to write.")
        return

    # Get all unique keys to create CSV headers
    headers = set()
    for contact in contacts:
        headers.update(contact.keys())

    headers = sorted(headers)  # Sort headers alphabetically

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(contacts)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_vcard = os.path.join(script_dir, "data", "contacts.vcf")  # Path to your vCard file
    output_csv = os.path.join(script_dir, "data", "contacts.csv")   # Path to the output CSV file

    # Ensure the "data" directory exists
    os.makedirs(os.path.join(script_dir, "data"), exist_ok=True)

    print("Parsing vCard file...")
    contacts = parse_vcard(input_vcard)

    print(f"Found {len(contacts)} contacts. Writing to CSV...")
    write_to_csv(contacts, output_csv)

    print(f"Contacts successfully written to {output_csv}")
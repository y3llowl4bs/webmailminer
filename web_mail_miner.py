import os
import requests
from bs4 import BeautifulSoup
import re

# Create a function to extract email addresses from a webpage
def extract_emails(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        emails = re.findall(email_pattern, str(soup))
        return emails
    else:
        print(f"Failed to retrieve the web page at {url}. Status code: {response.status_code}")
        return []

# Create a list to store all extracted emails
all_emails = []

# Prompt the user for input
input_mode = input("Do you want to input domains (I) or read from a file (F)? ").upper()

if input_mode == "I":
    # Ask the user to input domains
    domains_input = input("Enter the domains (comma-separated): ")
    domains = [domain.strip() for domain in domains_input.split(",")]
elif input_mode == "F":
    # Read domains from a file
    file_path = input("Enter the file path containing domains: ")
    with open(file_path, 'r') as file:
        domains = [line.strip() for line in file.readlines()]
else:
    print("Invalid input mode. Please use 'I' for user input or 'F' for file input.")
    exit()

# Loop through the list of domains
for domain in domains:
    url = f"https://www.{domain}"
    emails = extract_emails(url)
    all_emails.extend(emails)

# Define the output file path
output_file = os.path.join(os.path.dirname(os.path.abspath(__file__), "email_addresses.txt"))

# Save the extracted email addresses to a text file
with open(output_file, 'w') as file:
    for email in all_emails:
        file.write(email + '\n')
    print(f"Extracted email addresses saved to {output_file}")

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# Function to extract emails and phone numbers from the text
def extract_emails_and_phones(text):
    emails = re.findall(r'\S+@\S+', text)
    phones = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    return list(set(emails)), list(set(phones))

# Function to scrape contact info from specified divs
def scrape_contact_info_updated(url):
    try:
        response = requests.get(url, timeout=10)  # Set timeout to 10 seconds
        soup = BeautifulSoup(response.content, 'html.parser')

        contact_text = ''
        # Include the specified div classes
        for class_name in [
          "PartnershipAboutUs__ColAgents-sc-c433541d-6 ckMbEi"
        ]:
            divs = soup.find_all('div', class_=class_name)
            for div in divs:
                contact_text += div.get_text(separator=' ') + ' '

        emails, phones = extract_emails_and_phones(contact_text)
        return emails, phones
    except requests.exceptions.Timeout:
        print(f"Timeout while trying to access {url}")
        return [], []
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return [], []

# Load the Excel file
file_path = 'corcoran.xlsx'  # Update with your actual file path
df = pd.read_excel(file_path)

# Initialize lists to store email and phone results
all_emails_updated = []
all_phones_updated = []

# Iterate over the links in the first column
for index in range(len(df)):
    link = df.iloc[index, 0]  # Use .iloc to access by index
    emails, phones = scrape_contact_info_updated(link)
    
    all_emails_updated.append(', '.join(emails))
    all_phones_updated.append(', '.join(phones))

# Add updated results to DataFrame
df['Email'] = all_emails_updated
df['Phone'] = all_phones_updated

# Save the results to a new Excel file
output_file_path_updated = 'corcoran_cleaned_v5.xlsx'  # Update with your desired output path
df.to_excel(output_file_path_updated, index=False)

print(f"Scraped data saved to {output_file_path_updated}")

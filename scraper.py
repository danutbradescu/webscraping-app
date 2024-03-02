# scraper.py
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import csv

def read_website_list(file_path):
    """
    Reads a list of URLs from a .snappy.parquet file.
    """
    df = pd.read_parquet(file_path)
    print("Columns in DataFrame:", df.columns)
    column_name = 'domain'
    if column_name in df.columns:
        websites = df[column_name].tolist()
        return websites
    else:
        print(f"Column '{column_name}' not found in DataFrame.")
        return []

def scrape_website(url):
    """
    Attempts to scrape the given URL and returns a BeautifulSoup object.
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")
    return None

def find_contact_info(soup):
    """
    Finds and returns addresses, email addresses, and phone numbers from a BeautifulSoup object.
    """
    contact_info = {'address': None, 'email': None, 'phone': None}

    address_tag = soup.find('address')
    if address_tag:
        contact_info['address'] = address_tag.get_text(separator=' ', strip=True)

    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    phone_pattern = re.compile(r'\+?\d[\d -]{8,}\d')

    text = soup.get_text()
    email_matches = email_pattern.findall(text)
    phone_matches = phone_pattern.findall(text)

    if email_matches:
        contact_info['email'] = email_matches[0]
    if phone_matches:
        contact_info['phone'] = phone_matches[0]

    return contact_info

def scrape_to_csv(file_path, output_path='contact_info.csv', log_func=None):
    websites = read_website_list(file_path)
    all_contact_info = []

    for domain in websites:
        url = f'https://www.{domain}' if not domain.startswith('http://') and not domain.startswith('https://') else domain
        message = f"Scraping {url}"
        if log_func:
            log_func(message) 
        else:
            print(message)  
        soup = scrape_website(url)
        if soup:
            contact_info = find_contact_info(soup)
            contact_info['url'] = url
            all_contact_info.append(contact_info)

    # Additional messages and logic...
    if log_func:
        log_func("Scraping completed. The file is ready to use.")
    else:
        print("Scraping completed. The file is ready to use.")

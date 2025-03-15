import requests
from bs4 import BeautifulSoup
import csv
import time

# Function to fetch the data from the website
def fetch_data(url):
    try:
        # Send a GET request to the website
        response = requests.get(url)
        # Raise exception if the request was unsuccessful
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error while fetching data: {e}")
        return None

# Function to parse the HTML and extract data
def parse_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    quotes = []
    
    # Find all quotes on the page
    quote_divs = soup.find_all('div', class_='quote')
    for quote_div in quote_divs:
        quote_text = quote_div.find('span', class_='text').get_text()
        author = quote_div.find('small', class_='author').get_text()
        tags = [tag.get_text() for tag in quote_div.find_all('a', class_='tag')]
        
        quotes.append({
            'quote': quote_text,
            'author': author,
            'tags': ', '.join(tags)
        })
    return quotes

# Function to save the extracted data into a CSV file
def save_to_csv(data, filename):
    # Fieldnames for the CSV file
    fieldnames = ['quote', 'author', 'tags']
    
    try:
        # Open the CSV file in append mode and write the data
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            # Write header only if file is empty
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    except Exception as e:
        print(f"Error while saving data to CSV: {e}")

# Main function to drive the script
def main():
    base_url = 'http://quotes.toscrape.com/page/{}/'
    all_quotes = []
    
    for page_number in range(1, 6):  # Scraping first 5 pages as an example
        url = base_url.format(page_number)
        print(f"Scraping page {page_number}...")

        # Fetch the page content
        html = fetch_data(url)
        
        if html:
            quotes = parse_data(html)
            all_quotes.extend(quotes)
        time.sleep(1)  # Sleep to prevent overloading the server

    # Check data integrity
    if all_quotes:
        print(f"Scraping successful! Found {len(all_quotes)} quotes.")
        save_to_csv(all_quotes, 'quotes.csv')
    else:
        print("No data found!")

if __name__ == '__main__':
    main()

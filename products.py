import requests
from bs4 import BeautifulSoup
import csv

def scrape_product_details(url):
    response = requests.get(url)
    product_details = {}
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # ASIN
        asin = soup.select_one('[data-feature-name="ASIN"]')
        if asin:
            product_details['ASIN'] = asin.get('data-value', 'Not available')
        else:
            product_details['ASIN'] = 'Not available'
        
        # Product Description
        description = soup.find('div', {'id': 'productDescription'})
        product_details['Product Description'] = description.get_text(strip=True) if description else 'Not available'
        
        # Manufacturer
        manufacturer = soup.select_one('a[id="bylineInfo"]')
        product_details['Manufacturer'] = manufacturer.get_text(strip=True) if manufacturer else 'Not available'
    
    return product_details

if __name__ == "__main__":
    # Load the product URLs from the CSV file obtained in Part 1
    product_urls = []
    with open('amazon_bags_data.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            product_urls.append(row['Product URL'])
    
    all_product_details = []
    
    for url in product_urls:
        product_detail = scrape_product_details(url)
        all_product_details.append(product_detail)
    
    # Save the additional product details to a new CSV file
    with open('amazon_bags_product_details.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['ASIN', 'Product Description', 'Manufacturer']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in all_product_details:
            writer.writerow(item)

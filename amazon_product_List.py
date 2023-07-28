import requests
from bs4 import BeautifulSoup
import csv

def scrape_product_listing(url, num_pages=20):
    all_products = []
    
    for page_num in range(1, num_pages + 1):
        page_url = f"{url}&page={page_num}"
        response = requests.get(page_url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            product_items = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            for item in product_items:
                product_data = {}
                
                # Product URL
                product_data['Product URL'] = 'https://www.amazon.in' + item.find('a', {'class': 'a-link-normal'})['href']
                
                # Product Name
                product_data['Product Name'] = item.find('span', {'class': 'a-size-medium'}).text.strip()
                
                # Product Price
                price = item.find('span', {'class': 'a-offscreen'})
                product_data['Product Price'] = price.text.strip() if price else 'Not available'
                
                # Rating
                rating = item.find('span', {'class': 'a-icon-alt'})
                product_data['Rating'] = rating.text.strip() if rating else 'Not rated'
                
                # Number of reviews
                reviews = item.find('span', {'class': 'a-size-base'})
                product_data['Number of Reviews'] = reviews.text.strip() if reviews else '0'
                
                all_products.append(product_data)
        
    return all_products

if __name__ == "__main__":
    url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
    num_pages_to_scrape = 20
    
    product_data = scrape_product_listing(url, num_pages_to_scrape)
    
    # Save data to a CSV file
    with open('amazon_bags_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in product_data:
            writer.writerow(item)

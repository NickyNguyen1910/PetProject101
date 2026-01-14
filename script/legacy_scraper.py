import requests
from bs4 import BeautifulSoup

# PROBLEM 1: Hardcoded URLs (We want to discover these automatically)
URLS = [
    "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    "http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"
]

def run_manual_scrape():
    results = []
    print("Starting manual scrape...")
    
    for url in URLS:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('h1').text
            price = soup.find('p', class_='price_color').text
            
            results.append(f"{title} - {price}")
            print(f"Scraped: {title}")
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    # PROBLEM 2: Saving to a text file (We want a Database)
    with open("scraped_data.txt", "w") as f:
        for line in results:
            f.write(line + "\n")
            
    print("Saved to scraped_data.txt")

if __name__ == "__main__":
    run_manual_scrape()
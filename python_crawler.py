import requests
import json
from bs4 import BeautifulSoup

# PROBLEM 1: Hardcoded URLs (We want to discover these automatically)
URL = ["http://books.toscrape.com/"]

def run_automatic_scrape():
    results = []
    print("Starting automatic scrape...")
    



    for url in URL:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            all_books = soup.find_all("article", class_="product_pod")

            for book in all_books:
                title_tag = book.find("h3").find("a")
                title = title_tag["title"]
                price = book.find('p', class_='price_color').text
                availability = book.find('p', class_='instock availability').text.strip()
            
                book_data = {
                    "title": title,
                    "price": price,
                    "availability": availability
                }
                
                results.append(book_data)
                print(f"Scraped: {title}")
            pass
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    # PROBLEM 2: Saving to a text file (We want a Database)
    with open("scraped_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
            
    print("Saved to scraped_data.json")

if __name__ == "__main__":
    run_automatic_scrape()
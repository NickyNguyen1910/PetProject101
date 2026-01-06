import requests
import json
from bs4 import BeautifulSoup

def run_automatic_scrape():
    
    results = []
    print("Starting automatic scrape...")
    

    for i in range (1,6):
        url = f"http://books.toscrape.com/catalogue/page-{i}.html"
        
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            all_books = soup.find_all("article", class_="product_pod")

            for book in all_books:

                #Title
                title_tag = book.find("h3").find("a")
                title = title_tag["title"]

                #Link
                href = title_tag["href"]
                link = "http://books.toscrape.com/" + href

                #Price
                price = book.find("p", class_='price_color').text

                #Availability
                availability = book.find("p", class_='instock availability').text.strip()
                
                #Rating
                star_tag = book.find("p", class_="star-rating")
                rating_class = star_tag["class"][1]
                
                match rating_class:
                    case "One": rating = 1
                    case "Two": rating = 2
                    case "Three": rating = 3
                    case "Four": rating = 4
                    case "Five": rating = 5
                    
                #Image
                image_tag = book.find("img")
                img = image_tag["src"]
                image_url = "http://books.toscrape.com/" + img

                book_data = {
                    "title": title,
                    "price": price,
                    "availability": availability,
                    "rating": rating,
                    "image_url": image_url,
                    "book_url": link
                }
                results.append(book_data)

                
                
                print(f"Scraped: {title}")
            pass
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")


    with open("scraped_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
            
    print("Saved to scraped_data.json")


run_automatic_scrape()
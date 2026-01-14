import requests
import json
from bs4 import BeautifulSoup
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

def connect_to_db():

    print("Connecting to the database...")

    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_NAME"),
            user=os.getenv("POSTGRES_USER"),
            host=os.getenv("POSTGRES_HOST"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        print("ze bluetooth device iz connected successfully")
    except:
        print("Unable to connect to the database")
    return conn

def create_table(conn):

    print("Creating table...")

    with conn.cursor() as curs:

        try:
            curs.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id SERIAL PRIMARY KEY,
                    title TEXT,
                    price NUMERIC,
                    availability TEXT,
                    rating INTEGER,
                    image_url TEXT,
                    book_url TEXT UNIQUE
                );
                """)
            print("Table created successfully")

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    conn.commit()

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
                link = "http://books.toscrape.com/catalogue/" + href

                #Price
                price_dirty = book.find("p", class_='price_color').text
                price = price_dirty.replace("£", "")

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

            
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    with open("scraped_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
            
    print("Saved to scraped_data.json")
    return results


def insert_book(results, conn):
    with conn.cursor() as curs:

        try:

            for book_data in results: 

                curs.execute("""
                    INSERT INTO books (title, price, availability, rating, image_url, book_url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (book_url) DO NOTHING; 
                """, (book_data["title"],
                      book_data["price"],
                      book_data["availability"],
                      book_data["rating"],
                      book_data["image_url"],
                      book_data["book_url"]))
                    

            print("Book inserted successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        conn.commit() 



if __name__ == "__main__":
    conn = connect_to_db()
    create_table(conn)
    results = run_automatic_scrape()
    insert_book(results, conn)
    conn.close()

    
# PetProject101 - Book Crawler

A Python-based web scraper that automatically collects book information from [Books to Scrape](http://books.toscrape.com) and stores the data in both a PostgreSQL database and a local JSON file.

## Features

- **Automated Scraping**: Crawls through the first 5 pages of the catalogue(100 books).
- **Data Collection**: extracting title, price, availability, rating, image URL, and book URL.
- **Dual Storage**:
  - Saves raw data to `scraped_data.json`.
  - Persists structured data to a PostgreSQL `books` table.
- **Docker Support**: Containerized application for consistent execution environments.

## Prerequisites

- **Python**: Version 3.10 or higher.
- **PostgreSQL**: Version 17 or higher.
- **Docker**: Version 29.0 or higher (optional, for containerized run).

## Configuration

Create a `.env` file in the project root with your database credentials:

```env
DB_HOST=localhost
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_PORT=5432
```

## Local Installation & Usage

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Crawler**
   ```bash
   python python_crawler.py
   ```
   _The script will automatically attempt to connect to the database, create the `books` table if it doesn't exist, scrape data, and insert records._

## Docker Usage

1. **Build the Image**

   ```bash
   docker build -t python_crawler .
   ```

2. **Run the Container**
   ```bash
   docker run -it --rm --name python_crawler --env-file .env python_crawler
   ```
   _Note: Ensure your `.env` file is properly configured. If connecting to a database on the host machine from Docker, you may need to use `host.docker.internal` as the `DB_HOST`._

## Database Schema

The script creates a `books` table with the following structure:

| Column | Type | Description |
|README.md |------- |------------------------------|
| `id` | SERIAL | Primary Key |
| `title` | TEXT | Book title |
| `price` | NUMERIC | Price (without currency symbol)|
| `availability`| TEXT | Stock status |
| `rating` | INTEGER | 1-5 star rating |
| `image_url` | TEXT | URL of the book cover |
| `book_url` | TEXT | Unique URL of the book page |

## Output

- **Console**: Progress logs for database connection, table creation, scraping status, and insertion.
- **File**: `scraped_data.json` generated in the project root.
- **Database**: Populated `books` table.

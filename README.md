# Petlebi.com Product Information Scraper

This project is a scraper application to extract product information from petlebi.com and add it to a database by running an SQL file.

## Usage

1. Update your database connection information in the settings.py file

2. Run the scraper
   ```bash
   scrapy crawl products -o products.json

3. Update your database connection information in the settings.py file
  ```bash
  mysql -u username -p password database_name < database.sql

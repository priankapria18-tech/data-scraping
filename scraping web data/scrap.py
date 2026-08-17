import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://books.com.bd/List/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

books = []

# Change this according to the site's actual listing/search URL
for page in range(1, 5):

    url = f"{BASE_URL}/?page={page}"

    try:
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            print("Page failed:", page)
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        # Inspect the page and adjust selectors if necessary
        products = soup.select("div.c-info.text-center")

        for product in products:

            title_tag = product.select_one(
                "p.c-title.c-font-15.c-font-slim"
            )

            author_tag = product.select_one("p:not([class])")

            price_tag = product.select_one(
                "p.c-price.c-font-16.c-font-slim"
            )

            link_tag = product.select_one("a[href]")

            title = title_tag.get_text(" ", strip=True) if title_tag else ""
            author = author_tag.get_text(" ", strip=True) if author_tag else ""
            price = price_tag.get_text(" ", strip=True) if price_tag else ""

            book_url = ""

            if link_tag:
                book_url = link_tag.get("href", "")

                if book_url.startswith("/"):
                    book_url = BASE_URL + book_url

            if title:
                books.append({
                    "title": title,
                    "author": author,
                    "price": price,
                    "url": book_url
                })

        print(f"Page {page}: {len(books)} records collected")

        time.sleep(1)

    except Exception as e:
        print("Error:", e)

# Remove duplicates
df = pd.DataFrame(books)

df = df.drop_duplicates(
    subset=["title", "author"]
)

# Keep at least 2000 rows
df = df.head(2000)

df.to_csv(
    "books_dataset.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nScraping completed!")
print("Total rows:", len(df))
print("Dataset saved as books_dataset.csv")
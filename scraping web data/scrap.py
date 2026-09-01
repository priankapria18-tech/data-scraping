import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin

BASE_URL = "https://books.com.bd/List/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

books = []

for page in range(1, 12):

    url = f"{BASE_URL}?page={page}"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        if response.status_code != 200:
            print(f"Page {page} failed")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        products = soup.select("div.c-info.text-center")

        for product in products:

            title_tag = product.select_one(
                "p.c-title.c-font-15.c-font-slim"
            )

            author_tag = product.select_one(
                "p:not([class])"
            )

            price_tag = product.select_one(
                "p.c-price.c-font-16.c-font-slim"
            )

            # Find URL inside product
            link_tag = product.find("a", href=True)

            # If not found, check parent
            if not link_tag and product.parent:
                link_tag = product.parent.find("a", href=True)

            title = (
                title_tag.get_text(" ", strip=True)
                if title_tag else ""
            )

            author = (
                author_tag.get_text(" ", strip=True)
                if author_tag else ""
            )

            price = (
                price_tag.get_text(" ", strip=True)
                if price_tag else ""
            )

            book_url = ""

            if link_tag:
                book_url = link_tag.get("href", "").strip()

                # Convert relative URL to full URL
                book_url = urljoin(
                    "https://books.com.bd",
                    book_url
                )

            if title:
                books.append({
                    "title": title,
                    "author": author,
                    "price": price,
                    "url": book_url
                })

        print(
            f"Page {page}: "
            f"{len(books)} records collected"
        )

        time.sleep(1)

    except requests.RequestException as e:
        print(f"Error on page {page}: {e}")


# Create DataFrame
df = pd.DataFrame(books)

# Remove duplicates
df = df.drop_duplicates(
    subset=["title", "author"]
)

# Save CSV
df.to_csv(
    "books_dataset.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nScraping completed!")
print("Total rows:", len(df))
print("Dataset saved as books_dataset.csv")
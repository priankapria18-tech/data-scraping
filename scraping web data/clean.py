import pandas as pd
import re

# Load scraped dataset
df = pd.read_csv("books_dataset.csv")

print("Before Cleaning")
print("----------------")
print("Rows:", len(df))
print("\nMissing Values:")
print(df.isnull().sum())


# -----------------------------
# DATA CLEANING
# -----------------------------

# 1. Clean title
df["title"] = (
    df["title"]
    .fillna("")
    .astype(str)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)


# 2. Clean author
df["author"] = (
    df["author"]
    .fillna("Unknown")
    .astype(str)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)


# 3. Clean price
df["price"] = (
    df["price"]
    .fillna("")
    .astype(str)
    .str.replace("৳", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.extract(r"(\d+(?:\.\d+)?)")[0]
)

df["price"] = pd.to_numeric(
    df["price"],
    errors="coerce"
)


# 4. Clean URL
df["url"] = (
    df["url"]
    .fillna("")
    .astype(str)
    .str.strip()
)


# 5. Remove rows where title is empty
df = df[df["title"] != ""]


# 6. Remove invalid prices
df.loc[df["price"] <= 0, "price"] = pd.NA


# 7. Remove duplicate books
df = df.drop_duplicates(
    subset=["title", "author"]
)


# 8. Reset index
df = df.reset_index(drop=True)


# -----------------------------
# FINAL CHECK
# -----------------------------

print("\nAfter Cleaning")
print("----------------")
print("Rows:", len(df))

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nSample Cleaned Data:")
print(df.head(10))


# -----------------------------
# SAVE CLEANED DATASET
# -----------------------------

df.to_csv(
    "books_dataset_cleaned.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nData Cleaning Completed!")
print("Saved as: books_dataset_cleaned.csv")
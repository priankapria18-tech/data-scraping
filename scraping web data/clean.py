import pandas as pd
import re

# Load scraped dataset
df = pd.read_csv("books_dataset.csv")

print("Before Cleaning:")
print("Rows:", len(df))
print("\nMissing values:")
print(df.isnull().sum())


# -----------------------------
# DATA CLEANING
# -----------------------------

# 1. Remove duplicate records
df = df.drop_duplicates(
    subset=["title", "author"]
)


# 2. Clean title
df["title"] = (
    df["title"]
    .fillna("")
    .astype(str)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)


# 3. Clean author
df["author"] = (
    df["author"]
    .fillna("Unknown")
    .astype(str)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)


# 4. Clean price
df["price"] = (
    df["price"]
    .fillna("")
    .astype(str)
    .str.replace("৳", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.extract(r"(\d+(?:\.\d+)?)")[0]
)

# Convert price to numeric
df["price"] = pd.to_numeric(
    df["price"],
    errors="coerce"
)


# 5. Clean URL
df["url"] = (
    df["url"]
    .fillna("")
    .astype(str)
    .str.strip()
)


# 6. Remove records without title
df = df[df["title"] != ""]


# 7. Remove invalid prices
df.loc[df["price"] <= 0, "price"] = pd.NA


# 8. Remove duplicate records again
df = df.drop_duplicates(
    subset=["title", "author"]
)


# 9. Reset index
df = df.reset_index(drop=True)


# -----------------------------
# FINAL CHECK
# -----------------------------

print("\nAfter Cleaning:")
print("Rows:", len(df))

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nCleaned Dataset:")
print(df.head())


# -----------------------------
# SAVE CLEANED DATA
# -----------------------------

df.to_csv(
    "books_dataset_cleaned.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nData cleaning completed!")
print("Saved as: books_dataset_cleaned.csv")
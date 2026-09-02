import pandas as pd

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

# 1. Remove rows with missing values
df = df.dropna()

# 2. Clean title
df["title"] = (
    df["title"]
    .astype(str)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

# 3. Clean author
df["author"] = (
    df["author"]
    .astype(str)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

# 4. Clean price
df["price"] = (
    df["price"]
    .astype(str)
    .str.replace("৳", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.extract(r"(\d+(?:\.\d+)?)")[0]
)

df["price"] = pd.to_numeric(
    df["price"],
    errors="coerce"
)

# 5. Remove rows where price became missing
df = df.dropna()

# 6. Remove invalid price
df = df[df["price"] > 0]

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

print("\nCleaned Data:")
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
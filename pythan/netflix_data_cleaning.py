"""
Netflix Dataset - Data Cleaning Project
--------------------------------------
Requirements:
    pip install pandas

How to use:
    1. Keep this Python file and "netflix_data (1).csv" in the same folder.
    2. Run: python netflix_data_cleaning.py
    3. The cleaned file will be saved as "netflix_data_cleaned.csv".
"""

import pandas as pd
from pathlib import Path

# Step 1: Load the CSV file
input_file = Path("netflix_data (1).csv")
output_file = Path("netflix_data_cleaned.csv")

if not input_file.exists():
    raise FileNotFoundError(
        f"Could not find {input_file}. Put the CSV file in the same folder "
        "as this Python script, or update input_file with the correct path."
    )

df = pd.read_csv(input_file)

print("Original dataset shape:", df.shape)
print("\nOriginal missing values:")
print(df.isnull().sum())

# Step 2: Clean column names
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(r"\\s+", "_", regex=True)
)

# Step 3: Remove extra spaces from text columns
text_columns = df.select_dtypes(include=["object"]).columns
for column in text_columns:
    df[column] = df[column].str.strip()

# Step 4: Remove duplicate rows
duplicates_removed = df.duplicated().sum()
df = df.drop_duplicates()

# Step 5: Fill missing text values
columns_to_fill = ["director", "cast", "country", "rating", "duration"]
for column in columns_to_fill:
    if column in df.columns:
        df[column] = df[column].fillna("Unknown")

# Step 6: Convert date_added into a standard date format
if "date_added" in df.columns:
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    df["date_added"] = (
        df["date_added"].dt.strftime("%Y-%m-%d").fillna("Unknown")
    )

# Step 7: Convert release_year to numeric integer format
if "release_year" in df.columns:
    df["release_year"] = pd.to_numeric(
        df["release_year"], errors="coerce"
    ).astype("Int64")

# Step 8: Check remaining missing values
print("\nMissing values after cleaning:")
print(df.isnull().sum())

# Step 9: Save the cleaned dataset
df.to_csv(output_file, index=False)

# Step 10: Display final report
print("\nDATA CLEANING COMPLETED")
print("Rows and columns:", df.shape)
print("Duplicate rows removed:", duplicates_removed)
print("Cleaned file saved at:", output_file.resolve())

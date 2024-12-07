import pandas as pd
import re

input_file = "authors.csv"  
df = pd.read_csv(input_file, delimiter=";", encoding="ISO-8859-1")

def contains_invalid_chars(text):
    # Use a regular expression to match any non-standard character (non-ASCII)
    return bool(re.search(r'[^\x00-\x7F]+', str(text)))

df_cleaned = df[~df['about'].apply(contains_invalid_chars)]

output_file = "cleaned_authors.csv"
df_cleaned.to_csv(output_file, index=False, sep=";")

print(f"Cleaned data saved to {output_file}")

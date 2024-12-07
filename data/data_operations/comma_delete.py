import pandas as pd

input_file = "book.csv" 
output_file = "cleaned_book.csv"

# Read the CSV file with proper handling of quoted fields and commas inside the fields
try:
    df = pd.read_csv(input_file, delimiter=",", quoting=1, quotechar='"', on_bad_lines="skip")  # quoting=1 handles quoted fields
except pd.errors.ParserError as e:
    print(f"Error while parsing the file: {e}")
    exit()

# Remove commas from the related column if it exists
if "About" in df.columns:
    df["About"] = df["About"].str.replace(",", "", regex=False)

df.to_csv(output_file, index=False, quoting=1)  # quoting=1 ensures quotes are added for fields with special characters

print(f"Cleaned data saved to {output_file}")

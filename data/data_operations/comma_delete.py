import pandas as pd

input_file = "book.csv" 
output_file = "cleaned_book.csv"

try:
    df = pd.read_csv(input_file, delimiter=",", quoting=1, quotechar='"', on_bad_lines="skip")
except pd.errors.ParserError as e:
    print(f"Error while parsing the file: {e}")
    exit()

if "About" in df.columns:
    df["About"] = df["About"].str.replace(",", "", regex=False)

df.to_csv(output_file, index=False, quoting=1)

print(f"Cleaned data saved to {output_file}")

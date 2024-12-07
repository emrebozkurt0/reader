import pandas as pd

input_file = "data.csv"  
output_file = "cleaned_data.csv"

df = pd.read_csv(input_file, delimiter=";")

# Drop rows where the "comment_id" column is empty
column_name = "comment_id"
df = df[df[column_name].notna() & (df[column_name] != "")]

df.to_csv(output_file, index=False, sep=";")

print(f"Cleaned data without empty comment_id rows saved to {output_file}")

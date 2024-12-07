import pandas as pd
import numpy as np

input_file = "book.csv"
output_file = "book_with_rating.csv"

df = pd.read_csv(input_file, delimiter=";")

column_name = "Rating"
if column_name in df.columns:
    df[column_name] = df[column_name].apply(
        lambda x: np.random.randint(1, 6) if pd.isna(x) or x == "" else x
    )
else:
    print(f"The column '{column_name}' was not found in the file.")

df.to_csv(output_file, index=False, sep=";")

print(f"Updated data with random Ratings saved to {output_file}")

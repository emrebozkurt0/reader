import pandas as pd

input_file = "data/users_subscription.csv"  
output_file = "data/users_subscription.csv" 

df = pd.read_csv(input_file)

df["role"] = 0

df.to_csv(output_file, index=False)

print(f"'role' sütunu eklendi ve tüm değerler 0 olarak atandı. '{output_file}' dosyası oluşturuldu.")

import bcrypt
import pandas as pd

input_file = "users_subscription.csv"
output_file = "users_subscription.csv" 

def hash_password(password):
    """Hashes a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def process_csv(input_file, output_file):
    df = pd.read_csv(input_file, delimiter=';')

    if 'username' not in df.columns:
        raise ValueError("The column 'username' was not found in the input file.")

    df['password'] = df['username'].apply(hash_password)
    df.to_csv(output_file, index=False, sep=';')

if __name__ == "__main__":
    process_csv(input_file, output_file)
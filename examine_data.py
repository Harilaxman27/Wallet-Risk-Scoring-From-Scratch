import pandas as pd
import os

def examine_wallets_csv():
    """Examine the wallets.csv file to understand its structure"""
    
    csv_path = "data/raw/wallets.csv"
    
    # Check if file exists
    if not os.path.exists(csv_path):
        print("❌ wallets.csv not found!")
        print("Please put your wallets.csv file in the data/raw/ folder")
        return
    
    # Load and examine the CSV file
    try:
        df = pd.read_csv(csv_path)
        
        print("=== EXAMINING YOUR WALLETS.CSV FILE ===")
        print(f"📊 Number of wallets: {len(df)}")
        print(f"📋 Columns in the file: {list(df.columns)}")
        print(f"📁 File size: {os.path.getsize(csv_path)} bytes")
        
        print("\n=== FIRST 5 ROWS ===")
        print(df.head())
        
        print("\n=== FILE INFORMATION ===")
        print(df.info())
        
        print("\n=== CHECKING FOR MISSING VALUES ===")
        print(df.isnull().sum())
        
        # Check if addresses look valid
        if 'wallet_address' in df.columns:
            print("\n=== SAMPLE WALLET ADDRESSES ===")
            for i, addr in enumerate(df['wallet_address'].head(3)):
                print(f"{i+1}. {addr}")
        elif len(df.columns) == 1:
            # If there's only one column, assume it's wallet addresses
            col_name = df.columns[0]
            print(f"\n=== SAMPLE ADDRESSES FROM '{col_name}' COLUMN ===")
            for i, addr in enumerate(df[col_name].head(3)):
                print(f"{i+1}. {addr}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        return None

if __name__ == "__main__":
    examine_wallets_csv()

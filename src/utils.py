import pandas as pd
import numpy as np
from typing import List, Dict, Any
import re

def validate_ethereum_address(address: str) -> bool:
    """Validate Ethereum address format"""
    if not isinstance(address, str):
        return False
    if not address.startswith('0x'):
        return False
    if len(address) != 42:
        return False
    try:
        # Check if it's a valid hex
        int(address, 16)
        return True
    except ValueError:
        return False

def load_and_validate_wallets(csv_path: str) -> pd.DataFrame:
    """Load wallet addresses and validate them"""
    df = pd.read_csv(csv_path)
    
    print("=== WALLET VALIDATION ===")
    print(f"Total wallets loaded: {len(df)}")
    
    # Validate all addresses
    valid_addresses = []
    invalid_addresses = []
    
    for address in df['wallet_id']:
        if validate_ethereum_address(address):
            valid_addresses.append(address)
        else:
            invalid_addresses.append(address)
    
    print(f"✅ Valid addresses: {len(valid_addresses)}")
    print(f"❌ Invalid addresses: {len(invalid_addresses)}")
    
    if invalid_addresses:
        print("Invalid addresses found:")
        for addr in invalid_addresses:
            print(f"  - {addr}")
    
    return df

if __name__ == "__main__":
    df = load_and_validate_wallets("data/raw/wallets.csv")

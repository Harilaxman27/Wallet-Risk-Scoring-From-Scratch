import pandas as pd
import sys
import os
import time
from datetime import datetime

# Add src directory to path
sys.path.append('src')
from data_extraction import CompoundDataExtractor

def process_all_wallets():
    """Process all wallets and extract their data"""
    
    print("🚀 Starting batch processing of all wallets...")
    
    # Load wallet addresses
    df = pd.read_csv('data/raw/wallets.csv')
    wallets = df['wallet_id'].tolist()
    
    print(f"📊 Processing {len(wallets)} wallets...")
    
    # Initialize extractor
    extractor = CompoundDataExtractor()
    
    # Store results
    all_results = []
    
    # Process each wallet
    for i, wallet in enumerate(wallets, 1):
        print(f"\n[{i}/{len(wallets)}] Processing wallet: {wallet[:10]}...")
        
        try:
            result = extractor.extract_wallet_data(wallet)
            all_results.append(result)
            
            # Save progress every 10 wallets
            if i % 10 == 0:
                temp_df = pd.DataFrame(all_results)
                temp_df.to_csv('data/processed/temp_wallet_data.csv', index=False)
                print(f"💾 Progress saved: {i}/{len(wallets)} wallets processed")
            
            # Rate limiting - be nice to the API
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error processing {wallet}: {e}")
            # Add error entry to maintain order
            all_results.append({
                'wallet_address': wallet,
                'total_transactions': 0,
                'compound_transactions': 0,
                'error': str(e)
            })
    
    # Save final results
    final_df = pd.DataFrame(all_results)
    final_df.to_csv('data/processed/all_wallet_data.csv', index=False)
    
    print(f"\n✅ Batch processing complete!")
    print(f"📁 Results saved to: data/processed/all_wallet_data.csv")
    
    # Show summary statistics
    print("\n=== SUMMARY STATISTICS ===")
    print(f"Total wallets processed: {len(final_df)}")
    print(f"Wallets with Compound activity: {(final_df['compound_transactions'] > 0).sum()}")
    print(f"Average Compound transactions per active wallet: {final_df[final_df['compound_transactions'] > 0]['compound_transactions'].mean():.1f}")
    print(f"Total volume across all wallets: ${final_df['total_volume'].sum():,.2f}")
    
    return final_df

def process_sample_wallets(n=5):
    """Process just a few wallets for testing"""
    
    print(f"🧪 Processing first {n} wallets for testing...")
    
    # Load wallet addresses
    df = pd.read_csv('data/raw/wallets.csv')
    sample_wallets = df['wallet_id'].head(n).tolist()
    
    # Initialize extractor
    extractor = CompoundDataExtractor()
    
    # Store results
    results = []
    
    for i, wallet in enumerate(sample_wallets, 1):
        print(f"\n[{i}/{n}] Processing: {wallet[:10]}...")
        
        try:
            result = extractor.extract_wallet_data(wallet)
            results.append(result)
            time.sleep(1)  # Rate limiting
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                'wallet_address': wallet,
                'error': str(e)
            })
    
    # Save sample results
    sample_df = pd.DataFrame(results)
    sample_df.to_csv('data/processed/sample_wallet_data.csv', index=False)
    
    print(f"\n✅ Sample processing complete!")
    print(f"📁 Results saved to: data/processed/sample_wallet_data.csv")
    
    return sample_df

if __name__ == "__main__":
    # Choose what to run
    print("Choose processing option:")
    print("1. Process sample (5 wallets) - for testing")
    print("2. Process all wallets (103 wallets) - full run")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        results = process_sample_wallets()
    elif choice == "2":
        results = process_all_wallets()
    else:
        print("Invalid choice. Running sample by default.")
        results = process_sample_wallets()
    
    print("\n📊 First few results:")
    print(results.head())

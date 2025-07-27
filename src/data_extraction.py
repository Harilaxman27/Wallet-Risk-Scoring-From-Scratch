import requests
import pandas as pd
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
import sys
import os

# Add parent directory to path so we can import config
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import config

class CompoundDataExtractor:
    def __init__(self):
        self.alchemy_url = f"https://eth-mainnet.alchemyapi.io/v2/{config.ALCHEMY_API_KEY}"
        self.ctoken_addresses = [addr.lower() for addr in config.CTOKEN_ADDRESSES.values()]
        
    def get_wallet_transactions(self, wallet_address: str, max_pages: int = 5) -> List[Dict]:
        """Get all transactions for a wallet address"""
        print(f"📥 Fetching transactions for {wallet_address[:10]}...")
        
        all_transactions = []
        page_key = None
        
        for page in range(max_pages):
            payload = {
                "jsonrpc": "2.0",
                "method": "alchemy_getAssetTransfers",
                "params": [{
                    "fromBlock": "0x0",
                    "toBlock": "latest",
                    "fromAddress": wallet_address,
                    "category": ["external", "internal", "erc20", "erc721", "erc1155"],
                    "withMetadata": True,
                    "excludeZeroValue": False,
                    "maxCount": "0x3e8"  # 1000 transactions per page
                }],
                "id": 1
            }
            
            if page_key:
                payload["params"][0]["pageKey"] = page_key
                
            try:
                response = requests.post(self.alchemy_url, json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    if 'result' in result:
                        transfers = result['result']['transfers']
                        all_transactions.extend(transfers)
                        
                        # Check if there are more pages
                        if 'pageKey' in result['result']:
                            page_key = result['result']['pageKey']
                        else:
                            break
                    else:
                        print(f"❌ No result in response: {result}")
                        break
                else:
                    print(f"❌ HTTP error {response.status_code}")
                    break
                    
            except Exception as e:
                print(f"❌ Error fetching transactions: {e}")
                break
                
            # Rate limiting
            time.sleep(0.2)
            
        print(f"✅ Found {len(all_transactions)} total transactions")
        return all_transactions
    
    def filter_compound_transactions(self, transactions: List[Dict]) -> List[Dict]:
        """Filter transactions that interact with Compound protocol"""
        compound_txs = []
        
        for tx in transactions:
            # Check if transaction involves Compound cTokens
            to_address = tx.get('to', '').lower() if tx.get('to') else ''
            from_address = tx.get('from', '').lower() if tx.get('from') else ''
            
            if (to_address in self.ctoken_addresses or 
                from_address in self.ctoken_addresses or
                to_address == config.COMPOUND_V2_COMPTROLLER.lower()):
                
                compound_txs.append(tx)
                
        print(f"🔍 Found {len(compound_txs)} Compound-related transactions")
        return compound_txs
    
    def extract_wallet_data(self, wallet_address: str) -> Dict:
        """Extract and process all data for a single wallet"""
        
        # Get all transactions
        transactions = self.get_wallet_transactions(wallet_address)
        
        # Filter for Compound transactions
        compound_txs = self.filter_compound_transactions(transactions)
        
        # Basic metrics
        metrics = {
            'wallet_address': wallet_address,
            'total_transactions': len(transactions),
            'compound_transactions': len(compound_txs),
            'first_transaction': None,
            'last_transaction': None,
            'unique_tokens': set(),
            'total_volume': 0.0
        }
        
        if compound_txs:
            # Sort by block number
            compound_txs.sort(key=lambda x: int(x.get('blockNum', '0x0'), 16))
            
            metrics['first_transaction'] = compound_txs[0].get('metadata', {}).get('blockTimestamp')
            metrics['last_transaction'] = compound_txs[-1].get('metadata', {}).get('blockTimestamp')
            
            # Calculate volume and unique tokens
            for tx in compound_txs:
                if tx.get('asset'):
                    metrics['unique_tokens'].add(tx['asset'])
                if tx.get('value'):
                    try:
                        metrics['total_volume'] += float(tx['value'])
                    except:
                        pass
        
        metrics['unique_tokens'] = len(metrics['unique_tokens'])
        
        return metrics

def test_single_wallet():
    """Test the extractor with one wallet"""
    extractor = CompoundDataExtractor()
    
    # Test with the first wallet from your CSV
    test_wallet = "0x0039f22efb07a647557c7c5d17854cfd6d489ef3"
    
    print(f"🧪 Testing data extraction for wallet: {test_wallet}")
    
    result = extractor.extract_wallet_data(test_wallet)
    
    print("\n=== EXTRACTION RESULTS ===")
    for key, value in result.items():
        print(f"{key}: {value}")
    
    return result

if __name__ == "__main__":
    test_single_wallet()

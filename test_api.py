import config
import requests

def test_alchemy_connection():
    """Test if Alchemy API key is working"""
    
    print("=== TESTING ALCHEMY API CONNECTION ===")
    
    # Check if API key is loaded
    if not config.ALCHEMY_API_KEY:
        print("❌ API key not found in .env file")
        print("Make sure your .env file contains: ALCHEMY_API_KEY=your_key_here")
        return False
    
    print(f"✅ API key loaded (ends with: ...{config.ALCHEMY_API_KEY[-4:]})")
    
    # Test API connection with a simple request
    url = f"https://eth-mainnet.alchemyapi.io/v2/{config.ALCHEMY_API_KEY}"
    
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1
    }
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if 'result' in result:
                block_number = int(result['result'], 16)
                print(f"✅ API connection successful!")
                print(f"✅ Current block number: {block_number}")
                return True
            else:
                print(f"❌ API error: {result}")
                return False
        else:
            print(f"❌ HTTP error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    test_alchemy_connection()

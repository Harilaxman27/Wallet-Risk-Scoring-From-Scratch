# 🏦 DeFi Wallet Risk Scoring System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Ethereum](https://img.shields.io/badge/Blockchain-Ethereum-lightgrey.svg)](https://ethereum.org)

A comprehensive risk assessment pipeline that evaluates Ethereum wallet addresses based on their historical interactions with Compound V2/V3 lending protocols. Assigns risk scores from **0-1000** to enable data-driven lending decisions in DeFi.

## 🎯 Project Overview

This system analyzes **103 wallet addresses** and generates risk scores using a sophisticated **5-component scoring algorithm** that considers:

- **Activity Level** (25% weight) - Protocol engagement frequency
- **Transaction Volume** (20% weight) - Financial capacity indicators  
- **Experience** (20% weight) - Account age and market cycles survived
- **Diversification** (15% weight) - Multi-asset risk management
- **Consistency** (15% weight) - DeFi-focused behavior patterns

**Key Results:**
- ✅ **98% Success Rate** - 101/103 wallets successfully analyzed
- ✅ **$133M+ Volume** processed across all transactions
- ✅ **Realistic Distribution** - 8 high-risk, 86 medium-risk, 9 low-risk wallets

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** with pip
- **Git** for version control
- **Alchemy API account** ([Sign up free](https://www.alchemy.com/))

### Installation

1. Clone the repository
git clone https://github.com/<your-username>/wallet-risk-scoring.git
cd wallet-risk-scoring

2. Create and activate virtual environment
python -m venv venv

Windows
venv\Scripts\activate

macOS/Linux
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Configure API access
echo "ALCHEMY_API_KEY=your_alchemy_key_here" > .env


### Running the Analysis

Step 1: Extract blockchain data (20-25 minutes)
python process_all_wallets.py

→ Choose option 2 for full analysis of all 103 wallets
Step 2: Generate risk scores (30 seconds)
python src/risk_scoring.py


### Expected Outputs

- **`output/wallet_risk_scores.csv`** - Final deliverable (wallet_id, score)
- **`data/processed/detailed_risk_scores.csv`** - Component breakdown
- **`data/processed/all_wallet_data.csv`** - Raw blockchain data

## 📁 Project Structure

wallet-risk-scoring/
├── 📄 README.md # This file
├── 📄 requirements.txt # Python dependencies
├── 📄 config.py # Configuration settings
├── 📄 .env # API keys (local only)
├── 📄 .gitignore # Git ignore rules
├── 📄 process_all_wallets.py # Main data extraction script
├── 📄 examine_data.py # CSV file examination
├── 📄 test_api.py # API connectivity test
├── 📄 test_installation.py # Setup verification
├── 📁 data/
│ ├── 📁 raw/
│ │ └── 📄 wallets.csv # Input wallet addresses (103 wallets)
│ └── 📁 processed/ # Extracted blockchain data
├── 📁 src/
│ ├── 📄 init.py # Python package marker
│ ├── 📄 data_extraction.py # Blockchain data harvester
│ ├── 📄 risk_scoring.py # Risk assessment engine
│ └── 📄 utils.py # Helper functions
└── 📁 output/
└── 📄 wallet_risk_scores.csv # Final results (wallet_id, score)


## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

Required
ALCHEMY_API_KEY=your_alchemy_api_key_here

Optional (for Infura users)
INFURA_PROJECT_ID=your_infura_project_id_here

### Risk Scoring Weights

Modify `config.py` to adjust scoring parameters:

RISK_WEIGHTS = {
'activity_score': 250, # Max points for activity
'volume_score': 200, # Max points for volume
'experience_score': 200, # Max points for experience
'diversification_score': 150, # Max points for diversification
'consistency_score': 200 # Max points for consistency
}

## 📊 Understanding the Results

### Risk Score Interpretation

| Score Range | Risk Level | Description | Wallet Count |
|-------------|------------|-------------|--------------|
| **601-1000** | 🟢 **Low Risk** | Institutional-grade users | 9 (8.7%) |
| **301-600** | 🟡 **Medium Risk** | Typical retail DeFi users | 86 (83.5%) |
| **0-300** | 🔴 **High Risk** | New or inactive users | 8 (7.8%) |

### Sample Results

wallet_id,score
0x4814be12...,750
0x9e6ec4e9...,740
0x427f2ac5...,720
0x1656f188...,700


### Component Scores Breakdown

Each wallet receives individual scores for:

- **Activity Score** (0-250): Based on number of Compound transactions
- **Volume Score** (0-200): Based on total transaction volume 
- **Experience Score** (0-200): Based on account age and history
- **Diversification Score** (0-150): Based on unique tokens used
- **Consistency Score** (0-200): Based on DeFi engagement ratio

## 🧪 Testing & Validation

### Verify Setup
Test Python installation
python test_installation.py

Test API connectivity
python test_api.py

Examine input data
python examine_data.py


### Run Sample Analysis
Process just 5 wallets for testing
python process_all_wallets.py

→ Choose option 1 for sample run

## 🛠️ Technical Details

### Data Sources

- **Alchemy Ethereum API** - `alchemy_getAssetTransfers` endpoint
- **Compound Protocol** - V2 Comptroller and cToken contracts
- **Historical Data** - Full transaction history from 2019-2024

### Key Features

- **Batch Processing** - Progress saved every 10 wallets
- **Rate Limiting** - Respects API limits with intelligent delays
- **Error Handling** - Robust exception handling for network issues
- **Scalability** - Designed to handle 1000+ wallets efficiently

### Performance

- **Data Extraction**: ~15 seconds per wallet average
- **Risk Scoring**: <1 second per wallet
- **Memory Usage**: <100MB for full dataset
- **API Calls**: ~5-10 calls per wallet depending on activity

## 🚨 Troubleshooting

### Common Issues

**"No module named 'config'" Error:**
Ensure you're in the project root directory
cd wallet-risk-scoring
python src/risk_scoring.py

**API Key Not Found:**
Verify .env file exists and contains your key
cat .env # macOS/Linux
Get-Content .env # Windows PowerShell

**Low Success Rate:**
- Check internet connection
- Verify API key has sufficient credits
- Ensure wallet addresses are valid Ethereum addresses

**Empty Results:**
- Confirm input wallets have Compound protocol activity
- Check if wallets are active (not empty addresses)

## 🔐 Security Best Practices

- ✅ **Never commit `.env` files** to version control
- ✅ **Regenerate API keys** if accidentally exposed
- ✅ **Use environment variables** for all sensitive data
- ✅ **Regularly update dependencies** for security patches

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch** (`git checkout -b feature/enhancement`)
3. **Commit changes** (`git commit -am 'Add new feature'`)
4. **Push to branch** (`git push origin feature/enhancement`)
5. **Create Pull Request**

## 📈 Future Enhancements

- **Real-time Price Integration** - USD normalization via CoinGecko API
- **Multi-Protocol Support** - Aave, MakerDAO, Uniswap analysis
- **Machine Learning** - Predictive default probability modeling
- **Web Dashboard** - Streamlit-based interactive interface
- **API Deployment** - FastAPI microservice for production use

## 🙌 Credits

* Built for the **Zeru Internship Challenge**
* By: Salendra Harilaxman
*Last updated: July 27, 2025*



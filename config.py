import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
ALCHEMY_API_KEY = os.getenv('ALCHEMY_API_KEY')
INFURA_PROJECT_ID = os.getenv('INFURA_PROJECT_ID')

# Compound Protocol Addresses
COMPOUND_V2_COMPTROLLER = "0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B"
COMPOUND_V3_COMET_USDC = "0xc3d688B66703497DAA19211EEdff47f25384cdc3"

# cToken addresses for Compound V2 (most common ones)
CTOKEN_ADDRESSES = {
    'cUSDC': '0x39aa39c021dfbae8fac545936693ac917d5e7563',
    'cDAI': '0x5d3a536e4d6dbd6114cc1ead35777bab948e3643',
    'cETH': '0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5',
    'cUSDT': '0xf650c3d88d12db855b8bf7d11be6c55a4e07dcc9'
}

# Risk Scoring Weights
RISK_WEIGHTS = {
    'repayment_score': 0.3,
    'liquidation_score': 0.25,
    'stability_score': 0.2,
    'activity_score': 0.15,
    'diversification_score': 0.1
}

# File paths
WALLETS_CSV_PATH = "data/raw/wallets.csv"
OUTPUT_CSV_PATH = "output/wallet_risk_scores.csv"

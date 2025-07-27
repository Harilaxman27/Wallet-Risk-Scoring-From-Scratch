import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import config

class WalletRiskScorer:
    def __init__(self):
        self.weights = config.RISK_WEIGHTS
        
    def calculate_activity_score(self, row):
        """Calculate activity-based risk score (0-250 points)"""
        compound_txs = row['compound_transactions']
        
        # More transactions = lower risk (higher score)
        if compound_txs == 0:
            return 50  # No activity = high risk
        elif compound_txs >= 50:
            return 250  # Very active = low risk
        elif compound_txs >= 20:
            return 200
        elif compound_txs >= 10:
            return 160
        elif compound_txs >= 5:
            return 120
        else:
            return 80  # Low activity = higher risk
    
    def calculate_diversification_score(self, row):
        """Calculate diversification score (0-150 points)"""
        unique_tokens = row['unique_tokens']
        
        # More token diversity = lower risk (higher score)
        if unique_tokens >= 8:
            return 150
        elif unique_tokens >= 5:
            return 120
        elif unique_tokens >= 3:
            return 90
        elif unique_tokens >= 2:
            return 60
        else:
            return 30  # Single token = higher risk
    
    def calculate_volume_score(self, row):
        """Calculate volume-based score (0-200 points)"""
        volume = row['total_volume']
        
        # Higher volume users tend to be more sophisticated (lower risk)
        if volume >= 1000000:  # $1M+
            return 200
        elif volume >= 100000:  # $100K+
            return 170
        elif volume >= 10000:   # $10K+
            return 140
        elif volume >= 1000:    # $1K+
            return 110
        elif volume >= 100:     # $100+
            return 80
        else:
            return 50  # Very low volume = higher risk
    
    def calculate_experience_score(self, row):
        """Calculate experience score based on transaction history (0-200 points)"""
        first_tx = row['first_transaction']
        
        if pd.isna(first_tx) or first_tx is None:
            return 50  # No history = higher risk
        
        try:
            # Parse the timestamp
            first_date = pd.to_datetime(first_tx)
            current_date = pd.to_datetime('2024-01-01')  # Use a reference date
            
            # Calculate years of experience
            years = (current_date - first_date).days / 365.25
            
            if years >= 4:
                return 200  # Very experienced = low risk
            elif years >= 3:
                return 170
            elif years >= 2:
                return 140
            elif years >= 1:
                return 110
            else:
                return 70  # New user = higher risk
                
        except:
            return 50  # Error parsing = higher risk
    
    def calculate_consistency_score(self, row):
        """Calculate consistency score (0-200 points)"""
        compound_txs = row['compound_transactions']
        total_txs = row['total_transactions']
        
        if total_txs == 0:
            return 50
        
        # Ratio of compound to total transactions
        compound_ratio = compound_txs / total_txs
        
        if compound_ratio >= 0.5:
            return 200  # Very focused on DeFi = lower risk
        elif compound_ratio >= 0.2:
            return 160
        elif compound_ratio >= 0.1:
            return 120
        elif compound_ratio >= 0.05:
            return 80
        else:
            return 60  # Occasional DeFi user
    
    def calculate_wallet_risk_score(self, row):
        """Calculate overall risk score for a wallet (0-1000)"""
        
        # Calculate individual component scores
        activity_score = self.calculate_activity_score(row)
        diversification_score = self.calculate_diversification_score(row)
        volume_score = self.calculate_volume_score(row)
        experience_score = self.calculate_experience_score(row)
        consistency_score = self.calculate_consistency_score(row)
        
        # Sum all components (max possible = 1000)
        total_score = (
            activity_score +          # Max 250
            volume_score +            # Max 200  
            experience_score +        # Max 200
            diversification_score +   # Max 150
            consistency_score         # Max 200
        )
        
        # Ensure score is between 0 and 1000
        final_score = max(0, min(1000, int(total_score)))
        
        return {
            'score': final_score,
            'activity_score': activity_score,
            'volume_score': volume_score,
            'experience_score': experience_score,
            'diversification_score': diversification_score,
            'consistency_score': consistency_score
        }
    
    def score_all_wallets(self, data_file='data/processed/all_wallet_data.csv'):
        """Score all wallets and return results"""
        
        print("🧮 Starting risk scoring for all wallets...")
        
        # Load the extracted data
        df = pd.read_csv(data_file)
        
        print(f"📊 Scoring {len(df)} wallets...")
        
        results = []
        
        for idx, row in df.iterrows():
            wallet_address = row['wallet_address']
            
            # Calculate risk scores
            scores = self.calculate_wallet_risk_score(row)
            
            # Prepare result
            result = {
                'wallet_id': wallet_address,
                'score': scores['score']
            }
            
            # Add detailed scores for analysis
            result.update(scores)
            
            results.append(result)
            
            if (idx + 1) % 20 == 0:
                print(f"✅ Scored {idx + 1}/{len(df)} wallets...")
        
        results_df = pd.DataFrame(results)
        
        print(f"✅ Risk scoring complete!")
        
        return results_df

def generate_final_output():
    """Generate the final CSV output as required"""
    
    scorer = WalletRiskScorer()
    
    # Score all wallets
    scored_df = scorer.score_all_wallets()
    
    # Create the required output format (wallet_id, score)
    final_output = scored_df[['wallet_id', 'score']].copy()
    
    # Save the final output
    final_output.to_csv(config.OUTPUT_CSV_PATH, index=False)
    
    # Also save detailed scores for analysis
    scored_df.to_csv('data/processed/detailed_risk_scores.csv', index=False)
    
    print(f"\n📁 Final output saved to: {config.OUTPUT_CSV_PATH}")
    print(f"📁 Detailed scores saved to: data/processed/detailed_risk_scores.csv")
    
    # Show summary statistics
    print("\n=== RISK SCORING SUMMARY ===")
    print(f"Total wallets scored: {len(final_output)}")
    print(f"Average risk score: {final_output['score'].mean():.1f}")
    print(f"Median risk score: {final_output['score'].median():.1f}")
    print(f"Score range: {final_output['score'].min()} - {final_output['score'].max()}")
    
    print("\n=== SCORE DISTRIBUTION ===")
    print(f"High risk (0-300): {(final_output['score'] <= 300).sum()} wallets")
    print(f"Medium risk (301-600): {((final_output['score'] > 300) & (final_output['score'] <= 600)).sum()} wallets")
    print(f"Low risk (601-1000): {(final_output['score'] > 600).sum()} wallets")
    
    print(f"\n=== TOP 10 LOWEST RISK WALLETS ===")
    top_wallets = final_output.nlargest(10, 'score')
    for idx, row in top_wallets.iterrows():
        print(f"{row['wallet_id'][:10]}... : {row['score']}")
    
    print(f"\n=== TOP 10 HIGHEST RISK WALLETS ===")
    bottom_wallets = final_output.nsmallest(10, 'score')
    for idx, row in bottom_wallets.iterrows():
        print(f"{row['wallet_id'][:10]}... : {row['score']}")
    
    print("\n📊 Sample of final output:")
    print(final_output.head(10))
    
    return final_output

if __name__ == "__main__":
    generate_final_output()

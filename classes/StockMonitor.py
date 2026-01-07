import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import random
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
from collections import defaultdict
import warnings

from classes.StockPotentialAnalyzer import StockPotentialAnalyzer

warnings.filterwarnings('ignore')

class StockMonitor:
    """Monitor Saham secara berkala"""
    
    def __init__(self, symbols: List[str]):
        self.symbols = symbols
        self.analyzer = StockPotentialAnalyzer()
        self.history = []
        
    def run_single_analysis(self):
        """Run analysis for all symbols"""
        results = []
        
        for symbol in self.symbols:
            try:
                result = self.analyzer.analyze_stock(symbol)
                results.append(result)
                self.history.append(result)
                
                # Delay antara analisis saham
                time.sleep(1)
                
            except Exception as e:
                print(f"Error analyzing {symbol}: {e}")
        
        # Sort by potential score
        results.sort(key=lambda x: x['score_components']['total_score'], reverse=True)
        
        # Display ranking
        print(f"\n{'='*60}")
        print("STOCK RANKING BY POTENTIAL:")
        print(f"{'='*60}")
        
        for i, result in enumerate(results[:5], 1):
            score = result['score_components']['total_score']
            signal = result['recommendation']['signal']
            print(f"{i}. {result['symbol']}: {score:.1f} - {signal}")
        
        return results
    
    def run_continuous_monitoring(self, interval_minutes: int = 5):
        """Run continuous monitoring"""
        print(f"\nStarting continuous monitoring (interval: {interval_minutes} minutes)")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                print(f"\n{'='*60}")
                print(f"MONITORING CYCLE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"{'='*60}")
                
                self.run_single_analysis()
                
                print(f"\nNext update in {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")

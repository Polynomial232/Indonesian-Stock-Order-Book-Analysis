import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import random
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
from collections import defaultdict
import warnings

from classes.StockMonitor import StockMonitor

warnings.filterwarnings('ignore')

def main():
    """Main function"""
    
    # Daftar saham untuk dianalisis
    symbols = ['BBCA', 'BBRI', 'BMRI', 'TLKM', 'ASII', 'UNVR', 'ICBP', 'EXCL']
    
    # Inisialisasi monitor
    monitor = StockMonitor(symbols)
    
    print("STOCKBIT-INSPIRED STOCK ANALYSIS SYSTEM")
    print("=" * 60)
    print("\nFitur yang diimplementasikan:")
    print("1. Bandar Detector - Top Broker Asing")
    print("2. Bandar Detector - Broker Summary")
    print("3. Order Book Analysis dengan Bid/Ask")
    print("4. Fake Order Detection")
    print("5. Trading Recommendation dengan Entry, SL, TP")
    print("6. Continuous Monitoring")
    
    # Pilihan mode
    print(f"\n{'='*60}")
    print("SELECT MODE:")
    print("1. Single Analysis")
    print("2. Continuous Monitoring")
    print("3. Analyze Specific Stock")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        print("\nRunning single analysis...")
        monitor.run_single_analysis()
        
    elif choice == '2':
        interval = int(input("Enter monitoring interval (minutes): "))
        monitor.run_continuous_monitoring(interval)
        
    elif choice == '3':
        symbol = input("Enter stock symbol: ").upper()
        monitor.symbols = [symbol]
        monitor.run_single_analysis()
    
    else:
        print("Invalid choice. Running single analysis...")
        monitor.run_single_analysis()
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
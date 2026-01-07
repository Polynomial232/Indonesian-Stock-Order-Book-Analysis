import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import random
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')


class OrderBookAnalyzer:
    """Analisis Order Book dengan deteksi fake bid/ask"""
    
    def __init__(self):
        self.order_history = defaultdict(list)
        
    def generate_order_book(self, symbol: str) -> pd.DataFrame:
        """Generate dummy order book data"""
        bids = []
        asks = []
        
        # Generate bid side
        current_price = random.randint(1000, 2000)
        for i in range(10):
            price = current_price - i * 5
            volume = random.randint(100, 1000)
            bids.append({
                'price': price,
                'volume': volume,
                'type': 'BID'
            })
        
        # Generate ask side
        for i in range(10):
            price = current_price + i * 5
            volume = random.randint(100, 1000)
            asks.append({
                'price': price,
                'volume': volume,
                'type': 'ASK'
            })
        
        df_bids = pd.DataFrame(bids)
        df_asks = pd.DataFrame(asks)
        
        return pd.concat([df_bids, df_asks], ignore_index=True)
    
    def detect_fake_orders(self, order_book: pd.DataFrame, history_depth: int = 5) -> Dict:
        """Deteksi fake bid/ask berdasarkan perubahan tiba-tiba"""
        fake_signals = {
            'fake_bid': False,
            'fake_ask': False,
            'suspicious_level': 0,
            'details': []
        }
        
        # Simulasi deteksi fake orders
        bid_volumes = order_book[order_book['type'] == 'BID']['volume'].values
        ask_volumes = order_book[order_book['type'] == 'ASK']['volume'].values
        
        # Deteksi jika ada bid besar yang tiba-tiba hilang
        if len(bid_volumes) > 0:
            max_bid = np.max(bid_volumes)
            avg_bid = np.mean(bid_volumes)
            
            if max_bid > avg_bid * 3:
                fake_signals['fake_bid'] = True
                fake_signals['suspicious_level'] += 1
                fake_signals['details'].append(f"Large bid detected: {max_bid} vs avg {avg_bid:.0f}")
        
        # Deteksi jika ada ask besar yang tiba-tiba hilang
        if len(ask_volumes) > 0:
            max_ask = np.max(ask_volumes)
            avg_ask = np.mean(ask_volumes)
            
            if max_ask > avg_ask * 3:
                fake_signals['fake_ask'] = True
                fake_signals['suspicious_level'] += 1
                fake_signals['details'].append(f"Large ask detected: {max_ask} vs avg {avg_ask:.0f}")
        
        return fake_signals
    
    def calculate_order_book_imbalance(self, order_book: pd.DataFrame) -> float:
        """Hitung ketidakseimbangan order book"""
        total_bid = order_book[order_book['type'] == 'BID']['volume'].sum()
        total_ask = order_book[order_book['type'] == 'ASK']['volume'].sum()
        
        if total_bid + total_ask == 0:
            return 0
        
        imbalance = (total_bid - total_ask) / (total_bid + total_ask)
        return imbalance

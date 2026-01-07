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


class StockbitBandarDetector:
    """Simulasi Bandar Detector dari Stockbit"""
    
    def __init__(self):
        self.top_brokers = ['MACQUARIE', 'CITI', 'GOLDMAN', 'UBS', 'JPMORGAN', 'DEUTSCHE', 'HSBC', 'CREDIT SUISSE']
        self.local_brokers = ['MIRA', 'BRI', 'MANDIRI', 'BCA', 'BNI', 'CIMB', 'PANIN', 'DAWAH']
        
    def get_top_foreign_brokers(self) -> pd.DataFrame:
        """Data Top Broker Asing"""
        data = []
        for broker in self.top_brokers:
            data.append({
                'broker': broker,
                'net_buy_lots': random.randint(100, 1000),
                'total_value': random.randint(1e9, 1e10),
                'frequency': random.randint(10, 100),
                'trend': random.choice(['ACCUMULATION', 'DISTRIBUTION', 'NEUTRAL'])
            })
        return pd.DataFrame(data).sort_values('net_buy_lots', ascending=False)
    
    def get_broker_summary(self) -> pd.DataFrame:
        """Data Broker Summary"""
        data = []
        all_brokers = self.top_brokers + self.local_brokers
        
        for broker in all_brokers:
            buy_lots = random.randint(50, 800)
            sell_lots = random.randint(50, 800)
            net = buy_lots - sell_lots
            
            data.append({
                'broker': broker,
                'buy_lots': buy_lots,
                'sell_lots': sell_lots,
                'net_lots': net,
                'avg_price': random.randint(1000, 5000),
                'broker_type': 'FOREIGN' if broker in self.top_brokers else 'LOCAL'
            })
        
        df = pd.DataFrame(data)
        df['net_ratio'] = df['net_lots'] / (df['buy_lots'] + df['sell_lots'] + 1)
        return df.sort_values('net_lots', ascending=False)
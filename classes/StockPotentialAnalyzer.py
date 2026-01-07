import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import random
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
from collections import defaultdict
import warnings

from classes.StockbitBandarDetector import StockbitBandarDetector
from classes.OrderBookAnalyzer import OrderBookAnalyzer

warnings.filterwarnings('ignore')

class StockPotentialAnalyzer:
    """Analisis Potensi Saham"""
    
    def __init__(self):
        self.bandar_detector = StockbitBandarDetector()
        self.orderbook_analyzer = OrderBookAnalyzer()
        self.thresholds = {
            'min_foreign_net': 500,
            'min_imbalance': 0.3,
            'max_fake_level': 1,
            'min_broker_strength': 0.2
        }
    
    def analyze_stock(self, symbol: str) -> Dict:
        """Analisis lengkap untuk satu saham"""
        
        print(f"\n{'='*60}")
        print(f"ANALISIS SAHAM: {symbol}")
        print(f"{'='*60}")
        
        # 1. Data Top Broker Asing
        print("\n1. TOP BROKER ASING:")
        top_foreign = self.bandar_detector.get_top_foreign_brokers()
        print(top_foreign.head(5).to_string())
        
        foreign_net_total = top_foreign['net_buy_lots'].sum()
        foreign_strength = foreign_net_total / len(top_foreign)
        
        # 2. Data Broker Summary
        print("\n2. BROKER SUMMARY:")
        broker_summary = self.bandar_detector.get_broker_summary()
        print(broker_summary.head(10).to_string())
        
        # Pisahkan foreign vs local
        foreign_brokers = broker_summary[broker_summary['broker_type'] == 'FOREIGN']
        local_brokers = broker_summary[broker_summary['broker_type'] == 'LOCAL']
        
        foreign_net = foreign_brokers['net_lots'].sum()
        local_net = local_brokers['net_lots'].sum()
        
        # 3. Order Book Analysis
        print("\n3. ORDER BOOK ANALYSIS:")
        order_book = self.orderbook_analyzer.generate_order_book(symbol)
        
        print("Top 5 Bids:")
        print(order_book[order_book['type'] == 'BID'].head(5).to_string())
        print("\nTop 5 Asks:")
        print(order_book[order_book['type'] == 'ASK'].head(5).to_string())
        
        # Hitung imbalance
        imbalance = self.orderbook_analyzer.calculate_order_book_imbalance(order_book)
        print(f"\nOrder Book Imbalance: {imbalance:.2%}")
        
        # 4. Fake Order Detection
        fake_signals = self.orderbook_analyzer.detect_fake_orders(order_book)
        print("\n4. FAKE ORDER DETECTION:")
        print(f"Fake Bid Detected: {fake_signals['fake_bid']}")
        print(f"Fake Ask Detected: {fake_signals['fake_ask']}")
        print(f"Suspicious Level: {fake_signals['suspicious_level']}/2")
        if fake_signals['details']:
            for detail in fake_signals['details']:
                print(f"  - {detail}")
        
        # 5. Hitung Skor Potensi
        print(f"\n{'='*60}")
        print("POTENTIAL SCORE CALCULATION:")
        print(f"{'='*60}")
        
        # Komponen skor
        score_components = {}
        
        # 1. Foreign Accumulation (40%)
        foreign_score = min(foreign_strength / 500, 1.0) * 40
        score_components['foreign_accumulation'] = foreign_score
        print(f"Foreign Accumulation Score: {foreign_score:.1f}/40")
        
        # 2. Broker Imbalance (30%)
        broker_ratio = (foreign_net - local_net) / (abs(foreign_net) + abs(local_net) + 1)
        broker_score = (broker_ratio + 1) / 2 * 30
        score_components['broker_imbalance'] = broker_score
        print(f"Broker Imbalance Score: {broker_score:.1f}/30")
        
        # 3. Order Book Strength (20%)
        orderbook_score = max(imbalance, 0) * 20
        score_components['orderbook_strength'] = orderbook_score
        print(f"Order Book Strength Score: {orderbook_score:.1f}/20")
        
        # 4. Fake Order Penalty (-10 max)
        fake_penalty = fake_signals['suspicious_level'] * -5
        score_components['fake_order_penalty'] = fake_penalty
        print(f"Fake Order Penalty: {fake_penalty:.1f}")
        
        # Total Score
        total_score = sum(score_components.values())
        score_components['total_score'] = total_score
        
        print(f"\n{'='*60}")
        print(f"TOTAL POTENTIAL SCORE: {total_score:.1f}/100")
        
        # 6. Tentukan Signal dan Area Trading
        print(f"\n{'='*60}")
        print("TRADING RECOMMENDATION:")
        print(f"{'='*60}")
        
        recommendation = self.generate_recommendation(
            total_score, 
            foreign_net, 
            imbalance,
            fake_signals
        )
        
        # Tampilkan rekomendasi
        for key, value in recommendation.items():
            if key != 'score_components':
                print(f"{key.upper()}: {value}")
        
        # Simpan hasil analisis
        analysis_result = {
            'symbol': symbol,
            'timestamp': datetime.now(),
            'foreign_net': foreign_net,
            'local_net': local_net,
            'orderbook_imbalance': imbalance,
            'fake_signals': fake_signals,
            'score_components': score_components,
            'recommendation': recommendation
        }
        
        return analysis_result
    
    def generate_recommendation(self, total_score: float, foreign_net: float, 
                               imbalance: float, fake_signals: Dict) -> Dict:
        """Generate trading recommendation"""
        
        # Determine signal
        if total_score >= 70:
            signal = "STRONG BUY"
            confidence = "HIGH"
        elif total_score >= 50:
            signal = "BUY"
            confidence = "MEDIUM"
        elif total_score >= 30:
            signal = "NEUTRAL"
            confidence = "LOW"
        else:
            signal = "SELL"
            confidence = "HIGH"
        
        # Calculate price levels (dummy calculation)
        current_price = random.randint(1000, 2000)
        
        # Support and Resistance
        support = current_price * (1 - random.uniform(0.02, 0.05))
        resistance = current_price * (1 + random.uniform(0.02, 0.05))
        
        # Entry, Stop Loss, Take Profit
        if signal in ["STRONG BUY", "BUY"]:
            entry = current_price * (1 - random.uniform(0.005, 0.01))
            stop_loss = entry * (1 - random.uniform(0.03, 0.05))
            take_profit = entry * (1 + random.uniform(0.05, 0.08))
            position = "LONG"
        elif signal == "SELL":
            entry = current_price * (1 + random.uniform(0.005, 0.01))
            stop_loss = entry * (1 + random.uniform(0.03, 0.05))
            take_profit = entry * (1 - random.uniform(0.05, 0.08))
            position = "SHORT"
        else:
            entry = current_price
            stop_loss = current_price * (1 - 0.02)
            take_profit = current_price * (1 + 0.02)
            position = "WAIT"
        
        # Risk Reward Ratio
        risk = abs(entry - stop_loss)
        reward = abs(take_profit - entry)
        risk_reward = reward / risk if risk > 0 else 0
        
        recommendation = {
            'signal': signal,
            'confidence': confidence,
            'position': position,
            'current_price': current_price,
            'entry_area': f"{entry:.0f} - {entry * 1.005:.0f}",
            'stop_loss': f"{stop_loss:.0f}",
            'take_profit_1': f"{take_profit * 0.7:.0f}",
            'take_profit_2': f"{take_profit:.0f}",
            'risk_reward_ratio': f"{risk_reward:.2f}:1",
            'support': f"{support:.0f}",
            'resistance': f"{resistance:.0f}",
            'remarks': self.generate_remarks(signal, foreign_net, fake_signals)
        }
        
        return recommendation
    
    def generate_remarks(self, signal: str, foreign_net: float, fake_signals: Dict) -> str:
        """Generate remarks based on analysis"""
        remarks = []
        
        if signal in ["STRONG BUY", "BUY"]:
            if foreign_net > 1000:
                remarks.append("Strong foreign accumulation detected")
            elif foreign_net > 500:
                remarks.append("Moderate foreign buying")
        else:
            if foreign_net < -500:
                remarks.append("Foreign institutions are selling")
        
        if fake_signals['fake_bid']:
            remarks.append("Caution: Possible fake bids detected")
        if fake_signals['fake_ask']:
            remarks.append("Caution: Possible fake asks detected")
        
        if not remarks:
            remarks.append("No significant anomalies detected")
        
        return " | ".join(remarks)
from collections import defaultdict
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import numpy as np
from models import OrderBook, Order


class OrderBookAnalyzer:
    def __init__(self, history: List[OrderBook]):
        self.history = history
        self.lot_size = 1
        self.min_order_value = 50000000  # Minimal 50 juta rupiah untuk order signifikan
        
    def total_lot(self, orders: List[Order]) -> int:
        """Total lot dari list order"""
        return sum(o.lot for o in orders)
    
    def total_value(self, orders: List[Order]) -> float:
        """Total nilai rupiah dari list order"""
        return sum(o.lot * self.lot_size * o.price for o in orders)
    
    def bid_strength(self, ob: OrderBook) -> float:
        """Strength berdasarkan jumlah lot"""
        bid = self.total_lot(ob.bid)
        ask = self.total_lot(ob.ask)
        return bid / (bid + ask) if bid + ask > 0 else 0.0
    
    def bid_ask_ratio(self, ob: OrderBook) -> float:
        """Ratio berdasarkan lot"""
        ask = self.total_lot(ob.ask)
        return self.total_lot(ob.bid) / ask if ask > 0 else float("inf")
    
    def bid_value_ratio(self, ob: OrderBook) -> float:
        """Ratio berdasarkan nilai rupiah"""
        ask_value = self.total_value(ob.ask)
        return self.total_value(ob.bid) / ask_value if ask_value > 0 else float("inf")
    
    def spread(self, ob: OrderBook) -> int:
        """Spread dalam rupiah"""
        if not ob.ask or not ob.bid:
            return 0
        return ob.ask[0].price - ob.bid[0].price
    
    def spread_percentage(self, ob: OrderBook) -> float:
        """Spread dalam persentase"""
        if not ob.ask or not ob.bid or ob.bid[0].price == 0:
            return 0.0
        return (self.spread(ob) / ob.bid[0].price) * 100
    
    def strength_score(self, order: Order) -> int:
        """Skor strength dengan bobot yang disesuaikan"""
        return order.lot * order.freq * (1 if order.lot >= 100 else 0.5)
    
    def is_significant_order(self, order: Order) -> bool:
        """Cek apakah order signifikan (minimal 50 juta rupiah)"""
        order_value = order.lot * self.lot_size * order.price
        return order_value >= self.min_order_value
    
    def detect_fake_bid(self, lookback_period: int = 10) -> Dict:
        """
        Deteksi fake bid dengan kriteria:
        1. Order besar muncul tapi tidak sustain
        2. Sering dihapus atau dimodifikasi
        """
        if len(self.history) < lookback_period:
            lookback_period = len(self.history)
        
        fake_candidates = []
        recent_history = self.history[-lookback_period:]
        
        # Track order persistence
        order_persistence = defaultdict(list)
        
        for i, ob in enumerate(recent_history):
            for bid in ob.bid:
                if bid.lot >= 500 and bid.freq <= 2:  # Minimal 500 lot dengan freq rendah
                    order_persistence[bid.price].append(i)
        
        # Analyze persistence
        fake_prices = []
        for price, appearances in order_persistence.items():
            if len(appearances) <= 2:  # Muncul <= 2 kali dari lookback period
                fake_prices.append(price)
        
        return {
            "detected": len(fake_prices) > 0,
            "fake_prices": fake_prices,
            "count": len(fake_prices)
        }
    
    def detect_spoofing(self, lookback_period: int = 15) -> Dict:
        """
        Deteksi spoofing dengan pattern:
        1. Order besar muncul di level tertentu
        2. Kemudian di-cancel atau dihapus
        3. Pattern berulang di level yang berbeda
        """
        if len(self.history) < lookback_period:
            lookback_period = len(self.history)
        
        recent_history = self.history[-lookback_period:]
        spoofing_patterns = []
        
        # Track large orders and their behavior
        large_orders_timeline = defaultdict(list)
        
        for idx, ob in enumerate(recent_history):
            for bid in ob.bid:
                if bid.lot >= 1000 and self.is_significant_order(bid):
                    large_orders_timeline[bid.price].append(idx)
        
        # Check for spoofing patterns (order muncul lalu hilang berulang)
        for price, appearances in large_orders_timeline.items():
            if len(appearances) >= 3:
                # Check if there's a pattern of appearing and disappearing
                gaps = []
                for i in range(1, len(appearances)):
                    gaps.append(appearances[i] - appearances[i-1])
                
                # Jika jarak muncul-hilang konsisten, kemungkinan spoofing
                if len(gaps) >= 2 and max(gaps) - min(gaps) <= 2:
                    spoofing_patterns.append({
                        "price": price,
                        "appearances": appearances,
                        "pattern": "regular_cancellation"
                    })
        
        return {
            "detected": len(spoofing_patterns) > 0,
            "patterns": spoofing_patterns,
            "count": len(spoofing_patterns)
        }
    
    def get_market_depth(self, ob: OrderBook, depth: int = 5) -> Dict:
        """Get market depth sampai n level"""
        bid_depth = ob.bid[:depth] if len(ob.bid) >= depth else ob.bid
        ask_depth = ob.ask[:depth] if len(ob.ask) >= depth else ob.ask
        
        return {
            "bid_depth": [
                {
                    "price": b.price,
                    "lot": b.lot,
                    "freq": b.freq,
                    "value": b.lot * self.lot_size * b.price
                } for b in bid_depth
            ],
            "ask_depth": [
                {
                    "price": a.price,
                    "lot": a.lot,
                    "freq": a.freq,
                    "value": a.lot * self.lot_size * a.price
                } for a in ask_depth
            ]
        }
    
    def strongest_demand(self, depth: int = 3) -> Dict:
        """Strongest demand area (support zone)"""
        ob = self.history[-1]
        top_bids = sorted(ob.bid, key=self.strength_score, reverse=True)[:depth]
        
        total_lot = sum(b.lot for b in top_bids)
        total_value = sum(b.lot * self.lot_size * b.price for b in top_bids)
        avg_price = sum(b.price * b.lot for b in top_bids) / total_lot if total_lot > 0 else 0
        
        return {
            "prices": [b.price for b in top_bids],
            "total_lot": total_lot,
            "total_value": total_value,
            "avg_price": avg_price,
            "orders": [
                {
                    "price": b.price,
                    "lot": b.lot,
                    "freq": b.freq,
                    "score": self.strength_score(b)
                } for b in top_bids
            ]
        }
    
    def strongest_supply(self, depth: int = 3) -> Dict:
        """Strongest supply area (resistance zone)"""
        ob = self.history[-1]
        top_asks = sorted(ob.ask, key=self.strength_score, reverse=True)[:depth]
        
        total_lot = sum(a.lot for a in top_asks)
        total_value = sum(a.lot * self.lot_size * a.price for a in top_asks)
        avg_price = sum(a.price * a.lot for a in top_asks) / total_lot if total_lot > 0 else 0
        
        return {
            "prices": [a.price for a in top_asks],
            "total_lot": total_lot,
            "total_value": total_value,
            "avg_price": avg_price,
            "orders": [
                {
                    "price": a.price,
                    "lot": a.lot,
                    "freq": a.freq,
                    "score": self.strength_score(a)
                } for a in top_asks
            ]
        }
    
    def calculate_imbalance(self, ob: OrderBook) -> Dict:
        """Calculate order book imbalance"""
        bid_lot = self.total_lot(ob.bid)
        ask_lot = self.total_lot(ob.ask)
        
        bid_value = self.total_value(ob.bid)
        ask_value = self.total_value(ob.ask)
        
        total_lot = bid_lot + ask_lot
        total_value = bid_value + ask_value
        
        return {
            "lot_imbalance": (bid_lot - ask_lot) / total_lot if total_lot > 0 else 0,
            "value_imbalance": (bid_value - ask_value) / total_value if total_value > 0 else 0,
            "bid_lot": bid_lot,
            "ask_lot": ask_lot,
            "bid_value": bid_value,
            "ask_value": ask_value
        }
    
    def volume_profile(self, lookback: int = 20) -> Dict:
        """Analyze volume profile over lookback period"""
        if len(self.history) < lookback:
            lookback = len(self.history)
        
        volume_data = []
        for ob in self.history[-lookback:]:
            volume_data.append({
                "timestamp": ob.timestamp,
                "volume": ob.volume,
                "bid_strength": self.bid_strength(ob),
                "imbalance": self.calculate_imbalance(ob)["lot_imbalance"]
            })
        
        return {
            "lookback_period": lookback,
            "avg_volume": np.mean([v["volume"] for v in volume_data]),
            "volume_trend": "increasing" if volume_data[-1]["volume"] > volume_data[0]["volume"] else "decreasing",
            "data": volume_data
        }
    
    def bullish_score(self) -> Dict:
        """Calculate comprehensive bullish score"""
        if not self.history:
            return {"score": 0, "components": {}}
        
        ob = self.history[-1]
        score = 0
        max_score = 100
        components = {}
        
        # 1. Bid Strength (0-25 points)
        strength = self.bid_strength(ob)
        if strength > 0.7:
            score += 25
            components["bid_strength"] = 25
        elif strength > 0.6:
            score += 20
            components["bid_strength"] = 20
        elif strength > 0.5:
            score += 15
            components["bid_strength"] = 15
        else:
            components["bid_strength"] = 0
        
        # 2. Bid-Ask Ratio (0-20 points)
        ratio = self.bid_ask_ratio(ob)
        if ratio > 2.0:
            score += 20
            components["bid_ask_ratio"] = 20
        elif ratio > 1.5:
            score += 15
            components["bid_ask_ratio"] = 15
        elif ratio > 1.0:
            score += 10
            components["bid_ask_ratio"] = 10
        else:
            components["bid_ask_ratio"] = 0
        
        # 3. Spread (0-15 points)
        spread_pct = self.spread_percentage(ob)
        if spread_pct <= 0.5:
            score += 15
            components["spread"] = 15
        elif spread_pct <= 1.0:
            score += 10
            components["spread"] = 10
        elif spread_pct <= 1.5:
            score += 5
            components["spread"] = 5
        else:
            components["spread"] = 0
        
        # 4. Volume Strength (0-10 points)
        if ob.volume > 500_000:
            score += 10
            components["volume"] = 10
        elif ob.volume > 100_000:
            score += 5
            components["volume"] = 5
        else:
            components["volume"] = 0
        
        # 5. Market Depth Imbalance (0-10 points)
        imbalance = self.calculate_imbalance(ob)["lot_imbalance"]
        if imbalance > 0.2:
            score += 10
            components["imbalance"] = 10
        elif imbalance > 0.1:
            score += 5
            components["imbalance"] = 5
        else:
            components["imbalance"] = 0
        
        # 6. No Manipulation (0-20 points)
        fake_bid = self.detect_fake_bid()
        spoofing = self.detect_spoofing()
        
        if not fake_bid["detected"]:
            score += 10
            components["no_fake_bid"] = 10
        else:
            components["no_fake_bid"] = 0
            
        if not spoofing["detected"]:
            score += 10
            components["no_spoofing"] = 10
        else:
            components["no_spoofing"] = 0
        
        return {
            "score": score,
            "percentage": (score / max_score) * 100,
            "components": components,
            "fake_bid_detected": fake_bid["detected"],
            "spoofing_detected": spoofing["detected"]
        }
    
    def signal(self) -> Dict:
        """Generate comprehensive trading signal"""
        if not self.history:
            return {"signal": "NO_DATA", "confidence": 0}
        
        score_result = self.bullish_score()
        score = score_result["score"]
        fake_bid = score_result["fake_bid_detected"]
        spoofing = score_result["spoofing_detected"]
        
        # Check manipulation first
        if spoofing:
            signal = "SPOOFING_DETECTED"
            confidence = 0
        elif fake_bid:
            signal = "FAKE_BID_DETECTED"
            confidence = 0
        else:
            # Generate signal based on score
            if score >= 80:
                signal = "STRONG_BUY"
                confidence = min(100, score + 10)
            elif score >= 65:
                signal = "BUY"
                confidence = score
            elif score >= 50:
                signal = "HOLD_POSITIVE"
                confidence = score - 10
            elif score >= 40:
                signal = "NEUTRAL"
                confidence = 40
            elif score >= 30:
                signal = "CAUTION"
                confidence = 30
            else:
                signal = "SELL"
                confidence = max(0, 100 - score)
        
        # Add market context
        ob = self.history[-1]
        market_depth = self.get_market_depth(ob, 3)
        demand = self.strongest_demand(2)
        supply = self.strongest_supply(2)
        
        return {
            "signal": signal,
            "confidence": confidence,
            "score": score_result,
            "market_depth": market_depth,
            "support_zone": demand,
            "resistance_zone": supply,
            "spread": {
                "absolute": self.spread(ob),
                "percentage": self.spread_percentage(ob)
            },
            "recommendation": self._generate_recommendation(signal, demand, supply)
        }
    
    def _generate_recommendation(self, signal: str, demand: Dict, supply: Dict) -> str:
        """Generate trading recommendation based on signal"""
        recommendations = {
            "STRONG_BUY": "Consider entering long position with tight stop loss below support",
            "BUY": "Look for buying opportunities near support levels",
            "HOLD_POSITIVE": "Hold existing positions, consider taking partial profits",
            "NEUTRAL": "Wait for clearer signal, avoid new positions",
            "CAUTION": "Consider reducing position size or hedging",
            "SELL": "Consider exiting long positions or entering short",
            "FAKE_BID_DETECTED": "Wait for confirmation, avoid trading based on suspected fake bids",
            "SPOOFING_DETECTED": "High risk of manipulation, avoid trading"
        }
        
        base_rec = recommendations.get(signal, "No recommendation available")
        
        # Add price targets if available
        if signal in ["STRONG_BUY", "BUY"] and demand.get("prices"):
            support = min(demand["prices"])
            base_rec += f". Nearest support at {support}"
        
        if signal in ["SELL", "CAUTION"] and supply.get("prices"):
            resistance = max(supply["prices"])
            base_rec += f". Nearest resistance at {resistance}"
        
        return base_rec
    
    def get_summary(self) -> Dict:
        """Get complete order book analysis summary"""
        if not self.history:
            return {"error": "No historical data available"}
        
        current_ob = self.history[-1]
        signal_result = self.signal()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "current_price_levels": {
                "best_bid": current_ob.bid[0].price if current_ob.bid else 0,
                "best_ask": current_ob.ask[0].price if current_ob.ask else 0,
                "mid_price": (current_ob.bid[0].price + current_ob.ask[0].price) / 2 
                             if current_ob.bid and current_ob.ask else 0
            },
            "order_book_metrics": {
                "bid_strength": self.bid_strength(current_ob),
                "bid_ask_ratio": self.bid_ask_ratio(current_ob),
                "bid_value_ratio": self.bid_value_ratio(current_ob),
                "spread": self.spread(current_ob),
                "spread_percentage": self.spread_percentage(current_ob),
                "total_bid_lot": self.total_lot(current_ob.bid),
                "total_ask_lot": self.total_lot(current_ob.ask),
                "total_bid_value": self.total_value(current_ob.bid),
                "total_ask_value": self.total_value(current_ob.ask)
            },
            "market_manipulation": {
                "fake_bid": self.detect_fake_bid(),
                "spoofing": self.detect_spoofing()
            },
            "key_levels": {
                "strongest_demand": self.strongest_demand(3),
                "strongest_supply": self.strongest_supply(3)
            },
            "market_depth": self.get_market_depth(current_ob, 5),
            "imbalance": self.calculate_imbalance(current_ob),
            "volume_analysis": self.volume_profile(20),
            "trading_signal": signal_result
        }
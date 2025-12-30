from OrderBookAnalyzer import OrderBookAnalyzer
from models import Order, OrderBook
from apis.stockbit import get_market_mover, get_orderbook_companies
import time 

market_mover = get_market_mover()
market_mover_symbols = [data['stock_detail']['code'] for data in market_mover['data']['mover_list']]

for symbol in market_mover_symbols:
    order_book = get_orderbook_companies(symbol)

    histories = [
        OrderBook(
            bid=[
                Order(
                    price=int(bid['price']),
                    freq=int(bid['que_num']),
                    lot=int(bid['volume']) / 100
                ) for bid in order_book['data']['bid']
            ],
            ask=[
                Order(
                    price=int(offer['price']),
                    freq=int(offer['que_num']),
                    lot=int(offer['volume']) / 100
                ) for offer in order_book['data']['offer']
            ],
            last_price=int(order_book['data']['lastprice']),
            volume=int(order_book['data']['volume']),
        ) for i in range(2)
    ]

    analyzer = OrderBookAnalyzer(histories)

    if(analyzer.bullish_score()['score'] < 50):
        continue

    if(analyzer.detect_fake_bid()['detected']):
        continue

    if(analyzer.detect_spoofing()['detected']):
        continue

    print('='*100)
    print(symbol)
    print("Last Price   :", histories[-1].last_price)
    print("Bid Strength :", round(analyzer.bid_strength(histories[-1]) * 100, 2), "%")
    print("BullishScore :", analyzer.bullish_score()['score'])
    print("Signal       :", analyzer.signal()['signal'])
    print("Area BUY     :", max(analyzer.strongest_demand()['orders'], key=lambda x: x['score']))
    if analyzer.strongest_supply()['orders']:
        print("Area SELL    :", max(analyzer.strongest_supply()['orders'], key=lambda x: x['score']))
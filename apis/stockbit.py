import requests

def get_emitten_trending():
    response = requests.get('https://exodus.stockbit.com/emitten/trending',
        headers={
            'Origin': 'https://stockbit.com',
            'Referer': 'https://stockbit.com/',
            'Authorization': f'Bearer {},
            'User-Agent': 'Mozilla/5.0'
        }
    )
    return response.json()


def get_orderbook_companies(symbol):
    response = requests.get(f'https://exodus.stockbit.com/company-price-feed/v2/orderbook/companies/{symbol}',
        headers={
            'Origin': 'https://stockbit.com',
            'Referer': 'https://stockbit.com/',
            'Authorization': f'Bearer {},
            'User-Agent': 'Mozilla/5.0'
        }
    )
    return response.json()


def get_market_mover():
    response = requests.get('https://exodus.stockbit.com/order-trade/market-mover',
        params={
            'mover_type': 'MOVER_TYPE_TOP_GAINER',
            'filter_stocks': ['FILTER_STOCKS_TYPE_MAIN_BOARD', 'FILTER_STOCKS_TYPE_DEVELOPMENT_BOARD', 'FILTER_STOCKS_TYPE_ACCELERATION_BOARD', 'FILTER_STOCKS_TYPE_NEW_ECONOMY_BOARD']
        },
        headers={
            'Origin': 'https://stockbit.com',
            'Referer': 'https://stockbit.com/',
            'Authorization': f'Bearer {},
            'User-Agent': 'Mozilla/5.0'
        }
    )
    return response.json()
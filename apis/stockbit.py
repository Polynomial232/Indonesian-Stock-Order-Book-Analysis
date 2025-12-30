import requests

def get_emitten_trending():
    response = requests.get('https://exodus.stockbit.com/emitten/trending',
        headers={
            'Origin': 'https://stockbit.com',
            'Referer': 'https://stockbit.com/',
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3MDc0NjI3LTg4MWItNDQzZC04OTcyLTdmMmMzOTNlMzYyOSIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZSI6InBvbHlub21pYWwiLCJlbWEiOiJkYWZmYWRoaXlhNTBAZ21haWwuY29tIiwiZnVsIjoiTXVoYW1tYWQgRGFmZmEgRGhpeWEgVWxoYXEiLCJzZXMiOiJkVEZrOXdja3pNTGhyU1IyIiwiZHZjIjoiNTNkNDkyNDBiMzIzODAxZDcwNTI5MTdlMDUyZDExMDkiLCJ1aWQiOjM4MDkyMjIsImNvdSI6IlNHIn0sImV4cCI6MTc2NzEwNTQ0OCwiaWF0IjoxNzY3MDE5MDQ4LCJpc3MiOiJTVE9DS0JJVCIsImp0aSI6IjlmODU5YzEwLWU3MTktNDAzNS1hMDU3LWQxYTU3YjcxMGMxMiIsIm5iZiI6MTc2NzAxOTA0OCwidmVyIjoidjEifQ.XHdKRyCL4BUjtK8BvPF7G5x4JCQZwHZOlyKGKlaSENPzwEAWZX8Tx5UoLfxqcQtZaNmL7bMDzwfzMM50EAhj7hZZib65GGsmPpdrNX_uSSCM5U7wcwG6431O7Ee6gpTmbwTfGfh4bjUzQ3NQdeOI1GVaS1Em8aNlpZoikQLzqk35xsXsaVtbdq8LnNWQFjnecQx2ANz9i4Vm44Oc9_Q7_Fz-8ETx5kGGVXMnA0JKK2_UP4opL--bTj9QdxG_zrVkctYpR7Fqwa3IJhMCzn5GsDtvbIUfSyGytOA55OA7w5FxqNX59ADAXd55GRRhmvjHD7ZpI9bTyPWy9yLM_-sXjQ',
            'User-Agent': 'Mozilla/5.0'
        }
    )
    return response.json()


def get_orderbook_companies(symbol):
    response = requests.get(f'https://exodus.stockbit.com/company-price-feed/v2/orderbook/companies/{symbol}',
        headers={
            'Origin': 'https://stockbit.com',
            'Referer': 'https://stockbit.com/',
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3MDc0NjI3LTg4MWItNDQzZC04OTcyLTdmMmMzOTNlMzYyOSIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZSI6InBvbHlub21pYWwiLCJlbWEiOiJkYWZmYWRoaXlhNTBAZ21haWwuY29tIiwiZnVsIjoiTXVoYW1tYWQgRGFmZmEgRGhpeWEgVWxoYXEiLCJzZXMiOiJkVEZrOXdja3pNTGhyU1IyIiwiZHZjIjoiNTNkNDkyNDBiMzIzODAxZDcwNTI5MTdlMDUyZDExMDkiLCJ1aWQiOjM4MDkyMjIsImNvdSI6IlNHIn0sImV4cCI6MTc2NzEwNTQ0OCwiaWF0IjoxNzY3MDE5MDQ4LCJpc3MiOiJTVE9DS0JJVCIsImp0aSI6IjlmODU5YzEwLWU3MTktNDAzNS1hMDU3LWQxYTU3YjcxMGMxMiIsIm5iZiI6MTc2NzAxOTA0OCwidmVyIjoidjEifQ.XHdKRyCL4BUjtK8BvPF7G5x4JCQZwHZOlyKGKlaSENPzwEAWZX8Tx5UoLfxqcQtZaNmL7bMDzwfzMM50EAhj7hZZib65GGsmPpdrNX_uSSCM5U7wcwG6431O7Ee6gpTmbwTfGfh4bjUzQ3NQdeOI1GVaS1Em8aNlpZoikQLzqk35xsXsaVtbdq8LnNWQFjnecQx2ANz9i4Vm44Oc9_Q7_Fz-8ETx5kGGVXMnA0JKK2_UP4opL--bTj9QdxG_zrVkctYpR7Fqwa3IJhMCzn5GsDtvbIUfSyGytOA55OA7w5FxqNX59ADAXd55GRRhmvjHD7ZpI9bTyPWy9yLM_-sXjQ',
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
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3MDc0NjI3LTg4MWItNDQzZC04OTcyLTdmMmMzOTNlMzYyOSIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZSI6InBvbHlub21pYWwiLCJlbWEiOiJkYWZmYWRoaXlhNTBAZ21haWwuY29tIiwiZnVsIjoiTXVoYW1tYWQgRGFmZmEgRGhpeWEgVWxoYXEiLCJzZXMiOiJkVEZrOXdja3pNTGhyU1IyIiwiZHZjIjoiNTNkNDkyNDBiMzIzODAxZDcwNTI5MTdlMDUyZDExMDkiLCJ1aWQiOjM4MDkyMjIsImNvdSI6IlNHIn0sImV4cCI6MTc2NzEwNTQ0OCwiaWF0IjoxNzY3MDE5MDQ4LCJpc3MiOiJTVE9DS0JJVCIsImp0aSI6IjlmODU5YzEwLWU3MTktNDAzNS1hMDU3LWQxYTU3YjcxMGMxMiIsIm5iZiI6MTc2NzAxOTA0OCwidmVyIjoidjEifQ.XHdKRyCL4BUjtK8BvPF7G5x4JCQZwHZOlyKGKlaSENPzwEAWZX8Tx5UoLfxqcQtZaNmL7bMDzwfzMM50EAhj7hZZib65GGsmPpdrNX_uSSCM5U7wcwG6431O7Ee6gpTmbwTfGfh4bjUzQ3NQdeOI1GVaS1Em8aNlpZoikQLzqk35xsXsaVtbdq8LnNWQFjnecQx2ANz9i4Vm44Oc9_Q7_Fz-8ETx5kGGVXMnA0JKK2_UP4opL--bTj9QdxG_zrVkctYpR7Fqwa3IJhMCzn5GsDtvbIUfSyGytOA55OA7w5FxqNX59ADAXd55GRRhmvjHD7ZpI9bTyPWy9yLM_-sXjQ',
            'User-Agent': 'Mozilla/5.0'
        }
    )
    return response.json()
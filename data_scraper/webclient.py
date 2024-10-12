import requests
import os

# a web client for scraping the financial api data
class WebClient:
    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key
        self.api_url = base_url

    def get(self, endpoint, params=None):
        if self.api_key is None:
            self.api_key = os.getenv('API_KEY')
        
        if self.api_url is None:
            self.api_url = os.getenv('API_URL')
        
        if self.api_key is None:
            raise ValueError('API key is not set')
        
        if self.api_url is None:
            raise ValueError('API URL is not set')
        
        if params is None:
            params = {}
        params['apikey'] = self.api_key
        
        if endpoint is None:
            raise ValueError('No endpoint provided')
        
        # send the request
        response = requests.get(f"{self.api_url}/{endpoint}", params=params)
        
        # if the request was not successful, raise an error
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch data from {response.url}")
        
        return response.json()
    

    def get_quote(self, symbols: list):
        if len(symbols) == 0:
            raise ValueError('No symbols provided')
        elif len(symbols) == 1:
            return self.get(f"quote-short/{symbols[0]}")
        else:
            return self.get(f"quote-short/{','.join(symbols)}")
    

    def get_price_history(self, symbol, start_date, end_date):
        if symbol is None:
            raise ValueError('No symbol provided')
        elif start_date is None:
            raise ValueError('No start date provided')
        elif end_date is None:
            raise ValueError('No end date provided')
        
        return self.get(f"historical-price-full/{symbol}", {'from': start_date, 'to': end_date})


    def get_stock_list(self):
        return self.get('available-traded/list')
    

if __name__ == '__main__':
    client = WebClient(base_url='https://financialmodelingprep.com/api/v3')
    print(client.get_quote(['AAPL', 'GOOG', 'MSFT', 'TSLA']))
    print(client.get_price_history('AAPL', '2021-01-01', '2021-01-31'))
    # print(client.get_stock_list())

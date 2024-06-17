import pandas as pd
import requests as r
from bs4 import BeautifulSoup
from dataclasses import dataclass

# >>> CLASSES <<<
# Stock -> Position -> Portifolio
# ==============================================================================
@dataclass
class Stock():
    ticker: str
    exchange: str
    price: float = 0
    currency: str = 'USD'
    usd_price: float = 0

    def __post_init__(self):
        price_info = get_price_information(ticker=self.ticker,
                                           exchange=self.exchange)
        self.price = price_info['price']
        self.currency = price_info['currency']
        self.usd_price = price_info['usd_price']

# ==============================================================================
@dataclass
class Position():
    stock: Stock
    quantity: int

# ==============================================================================
@dataclass
class Portfolio():
    positions: list[Position]

    def get_total_value(self):
        total_value = 0
        for position in self.positions:
            total_value += position.quantity * position.stock.usd_price
        return total_value



#  >>> FUNCTIONS <<<
# ------------------------------------------------------------------------------
def get_fx_to_usd(currency):
    fx_url = f'https://www.google.com/finance/quote/{currency}-USD'
    response = r.get(fx_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    fx_rate = soup.find('div', attrs={'data-last-price':True})
    fx = fx_rate['data-last-price']
    return float(fx)

# ------------------------------------------------------------------------------
def get_price_information(ticker, exchange):
    url = f'http://www.google.com/finance/quote/{ticker}:{exchange}'
    response = r.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    price_div = soup.find('div', attrs={'data-last-price':True})
    price = float(price_div['data-last-price'])
    currency = str(price_div['data-currency-code'])

    usd_price = price
    if currency != 'USD':
        fx = get_fx_to_usd(currency)
        usd_price = round(price*fx,2)

    return {
        'ticker':ticker,
        'exchange':exchange,
        'price':price,
        'currency':currency,
        'usd_price': usd_price
    }

# ------------------------------------------------------------------------------
def display_portfolio_summary(portfolio):
    if not isinstance(portfolio, Portfolio):
        raise TypeError('Please, Provide an Instance of Potfolio Type')
    
    portfolio_value = portfolio.get_total_value()
    position_data = []
    for position in portfolio.positions:
        position_data.append([
            position.stock.ticker,
            position.stock.exchange,
            position.quantity,
            position.stock.usd_price,
            position.quantity * position.stock.usd_price,
            round(position.quantity * position.stock.usd_price / portfolio_value * 100,2)
        ])

    df = pd.DataFrame(position_data)
    df.columns = ['Ticker',
                  'Exchange',
                  'Quantity',
                  'USD Price',
                  'Market Value',
                  'Percentage']
    print(df)
    print(f'Total Portifolio Value:', portfolio_value, '\n')



# >>> TEST <<<
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    shop = Stock('SHOP', 'TSE')
    msft = Stock('MSFT', 'NASDAQ')
    googl = Stock('GOOGL', 'NASDAQ')
    bns = Stock('BNS', 'TSE')

    positions = [Position(shop, 10),
                 Position(msft, 2),
                 Position(bns, 100),
                 Position(googl, 30)]
    
    portfolio = Portfolio(positions)

    display_portfolio_summary(portfolio)
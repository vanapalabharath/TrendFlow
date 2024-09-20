import requests
import json
import argparse
from datetime import datetime, timedelta

with open('mapping_dict.json', 'r') as f:
    mapping_dict = json.load(f)

date_format = '%Y-%m-%d'
today = datetime.now()
to_date = today.strftime(date_format)
start_date = today - timedelta(days=365)
from_date = start_date.strftime(date_format)

def fetch_data(instrument_key, from_date, to_date):
    interval = 'day'
    url = f"https://api.upstox.com/v2/historical-candle/{instrument_key}/{interval}/{to_date}/{from_date}"
    headers = {
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        candles = data.get('data', {}).get('candles', [])
        return candles
    except requests.RequestException:
        return []

def calculate_ema(prices, days):
    if len(prices) < days:
        return None
    k = 2 / (days + 1)
    ema = prices[0]  # Start with the first price
    for price in prices:
        ema = (price * k) + (ema * (1 - k))
    return ema

parser = argparse.ArgumentParser(description='Identify stocks with golden or death EMAs crossovers.')
parser.add_argument('symbol', type=str, nargs='?', help='The stock symbol to filter. If not provided, processes all symbols.')
args = parser.parse_args()

def process_symbols(symbols_dict, specific_symbol=None):
    for symbol, instrument_key in symbols_dict.items():
        if specific_symbol and symbol != specific_symbol:
            continue
        
        candles = fetch_data(instrument_key, from_date, to_date)
        if len(candles) < 200:
            continue
        
        closing_prices = [candle[4] for candle in candles]
        
        previous_50_ema = calculate_ema(closing_prices[1:51], 50)
        previous_200_ema = calculate_ema(closing_prices[1:201], 200)
        
        latest_50_ema = calculate_ema(closing_prices[:50], 50)
        latest_200_ema = calculate_ema(closing_prices[:200], 200)
        
        if previous_50_ema is not None and previous_200_ema is not None and latest_50_ema is not None and latest_200_ema is not None:
            crossover_type = None
            if previous_50_ema < previous_200_ema and latest_50_ema > latest_200_ema:
                crossover_type = "Golden Crossover"
            elif previous_50_ema > previous_200_ema and latest_50_ema < latest_200_ema:
                crossover_type = "Death Crossover"
            
            if crossover_type:
                print(f"Stock Name: {symbol}")
                print(f"Crossover Type: {crossover_type}")
                print(f"Previous 50-day EMA: {previous_50_ema:.2f}")
                print(f"Previous 200-day EMA: {previous_200_ema:.2f}")
                print(f"Latest 50-day EMA: {latest_50_ema:.2f}")
                print(f"Latest 200-day EMA: {latest_200_ema:.2f}")
                print('-' * 30)

process_symbols(mapping_dict, specific_symbol=args.symbol)

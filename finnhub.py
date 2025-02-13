import yfinance as yf

def fetch_yahoo_stock():
    symbol = '7113.KL'  # Example: Maybank on KLSE

    stock = yf.Ticker(symbol)

    stock_info = stock.history(period='1d')

    if not stock_info.empty:
        latest_data = stock_info.iloc[-1]
        print(f"Stock: {symbol}")
        print(f"Date: {latest_data.name.date()}")
        print(f"Open: {latest_data['Open']}")
        print(f"High: {latest_data['High']}")
        print(f"Low: {latest_data['Low']}")
        print(f"Close: {latest_data['Close']}")
        print(f"Volume: {latest_data['Volume']}")
    else:
        print("No data found for this stock.")

fetch_yahoo_stock()

print("The Next Line/n")

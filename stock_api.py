from flask import Flask, request, jsonify
import yfinance as yf
import os

app = Flask(__name__)

@app.route('/historical', methods=['GET'])
def get_historical_data():
    symbol = request.args.get('symbol', '7113.KL')
    period = request.args.get('period', '1mo')
    interval = request.args.get('interval', '1d')

    try:
        stock = yf.Ticker(symbol)
        stock_history = stock.history(period=period, interval=interval)

        if stock_history.empty:
            return jsonify({'error': 'No data found'}), 404

        data_list = []
        for date, row in stock_history.iterrows():
            data_list.append({
                'date': date.strftime('%Y-%m-%d'),
                'open': row['Open'],
                'high': row['High'],
                'low': row['Low'],
                'close': row['Close'],
                'volume': int(row['Volume'])
            })

        return jsonify(data_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

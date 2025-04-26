from flask import Flask, render_template, request
import pygal
import requests

app = Flask(__name__)

def get_stock_data(symbol):
    api_key = "YOUR_API_KEY"
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

def create_stock_chart(symbol):
    data = get_stock_data(symbol)
    
    if "Time Series (Daily)" not in data:
        return None
    
    timeseries = data["Time Series (Daily)"]
    dates = []
    closing_prices = []
    
    for date, values in timeseries.items():
        dates.append(date)
        closing_prices.append(float(values["4. close"]))
    
    line_chart = pygal.Line()
    line_chart.title = f"Stock Prices for {symbol}"
    line_chart.x_labels = dates[:10]
    line_chart.add(f"Closing Prices for {symbol}", closing_prices[:10])
    
    return line_chart.render_data_uri()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        stock_symbol = request.form["stock_symbol"]
        chart = create_stock_chart(stock_symbol)
        if chart:
            return render_template("index.html", chart=chart, stock_symbol=stock_symbol)
        else:
            return render_template("index.html", error="Invalid stock symbol or data not found.")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

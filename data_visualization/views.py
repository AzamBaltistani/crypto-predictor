import pandas as pd
import plotly.graph_objects as go
from django.shortcuts import render
from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

def visualize_crypto_data(request):
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("BINANCE_SECRET")
    client = Client(api_key, api_secret)

    # Get user input
    crypto_symbol = request.GET.get("crypto", "BTCUSDT")
    interval = request.GET.get("interval", "1d")
    start_date = request.GET.get("start_date", "01 Jan 2023")
    end_date = request.GET.get("end_date", "01 Jan 2024")

    # Fetch historical data
    historical = client.get_historical_klines(
        symbol=crypto_symbol, interval=interval, start_str=start_date, end_str=end_date
    )

    df = pd.DataFrame(historical, columns=["Time", "Open", "High", "Low", "Close", "Volume", "_", "_", "_", "_", "_", "_"])
    df["Time"] = pd.to_datetime(df["Time"], unit="ms")
    df["Open"] = pd.to_numeric(df["Open"])
    df["High"] = pd.to_numeric(df["High"])
    df["Low"] = pd.to_numeric(df["Low"])
    df["Close"] = pd.to_numeric(df["Close"])
    df["Volume"] = pd.to_numeric(df["Volume"])

    # 📌 Create Candlestick Chart using Plotly
    fig = go.Figure(data=[go.Candlestick(
        x=df["Time"],
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Candlestick"
    )])

    fig.update_layout(
        title=f"{crypto_symbol} Price Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False
    )

    # Convert Plotly figure to JSON
    chart_json = fig.to_json()

    return render(request, "data_visualization/chart.html", {"chart_json": chart_json})

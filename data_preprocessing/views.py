import pandas as pd
# import talib
from django.shortcuts import render
from django.http import JsonResponse
from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

def preprocess_crypto_data(request):
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("BINANCE_SECRET")
    client = Client(api_key, api_secret)

    # Get user input from query parameters
    crypto_symbol = request.GET.get("crypto", "BTCUSDT")
    interval = request.GET.get("interval", "1d")
    start_date = request.GET.get("start_date", "01 Jan 2023")
    end_date = request.GET.get("end_date", "01 Jan 2024")

    # Fetch historical data from Binance
    historical = client.get_historical_klines(
        symbol=crypto_symbol, interval=interval, start_str=start_date, end_str=end_date
    )

    df = pd.DataFrame(historical, columns=["Time", "Open", "High", "Low", "Close", "Volume", "_", "_", "_", "_", "_", "_"])
    df["Time"] = pd.to_datetime(df["Time"], unit="ms")

    # Convert price columns to numeric
    df["Open"] = pd.to_numeric(df["Open"])
    df["High"] = pd.to_numeric(df["High"])
    df["Low"] = pd.to_numeric(df["Low"])
    df["Close"] = pd.to_numeric(df["Close"])
    df["Volume"] = pd.to_numeric(df["Volume"])

    # 📌 Calculate Technical Indicators
    # df["SMA_10"] = talib.SMA(df["Close"], timeperiod=10)  # 10-day Simple Moving Average
    # df["EMA_10"] = talib.EMA(df["Close"], timeperiod=10)  # 10-day Exponential Moving Average
    # df["RSI"] = talib.RSI(df["Close"], timeperiod=14)  # Relative Strength Index (14-day)
    
    # # MACD Indicator
    # df["MACD"], df["MACD_Signal"], df["MACD_Hist"] = talib.MACD(df["Close"], fastperiod=12, slowperiod=26, signalperiod=9)

    # # Convert dataframe to JSON for frontend
    processed_data = df.to_dict(orient="records")

    return JsonResponse({"crypto": crypto_symbol, "data": processed_data})

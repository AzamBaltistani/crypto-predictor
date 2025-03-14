import os
import pandas as pd
from binance.client import Client
from django.shortcuts import render
from dotenv import load_dotenv

load_dotenv()

def fetch_crypto_data(request):
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("BINANCE_SECRET")
    client = Client(api_key, api_secret)

    crypto_symbol = request.GET.get("crypto", "BTCUSDT")
    interval = request.GET.get("interval", "1d")
    start_date = request.GET.get("start_date", "01 Jan 2023")
    end_date = request.GET.get("end_date", "01 Jan 2024")

    historical = client.get_historical_klines(
        symbol=crypto_symbol, interval=interval, start_str=start_date, end_str=end_date
    )

    df = pd.DataFrame(historical, columns=["Time", "Open", "High", "Low", "Close", "Volume", "_", "_", "_", "_", "_", "_"])
    df["Time"] = pd.to_datetime(df["Time"], unit="ms")

    context = {"crypto": crypto_symbol, "df": df.to_html()}
    return render(request, "data_fetching/fetch.html", context)


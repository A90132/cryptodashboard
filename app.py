import requests
import streamlit as st
import time

st.title("Crypto Buy vs Sell Pressure")

def get_binance_pressure(symbol="BTCUSDT", limit=500):
    url = f"https://api.binance.com/api/v3/trades?symbol={symbol}&limit={limit}"
    data = requests.get(url).json()

    buy_volume = 0
    sell_volume = 0

    for trade in data:
        qty = float(trade["qty"])
        if trade["isBuyerMaker"]:
            sell_volume += qty
        else:
            buy_volume += qty

    total = buy_volume + sell_volume

    return (buy_volume / total) * 100, (sell_volume / total) * 100

symbol = st.text_input("Symbol", "BTCUSDT")

placeholder = st.empty()

while True:
    buy, sell = get_binance_pressure(symbol)

    with placeholder.container():
        st.metric("Buy Pressure", f"{buy:.2f}%")
        st.metric("Sell Pressure", f"{sell:.2f}%")
        st.progress(int(buy))

    time.sleep(5)

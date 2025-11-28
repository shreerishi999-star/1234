import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Market Dashboard", layout="wide")

# ----------------------------
# HEADER
# ----------------------------
st.title("📊 Stock Market Dashboard (Streamlit)")

# ----------------------------
# USER INPUT
# ----------------------------
ticker = st.text_input("Enter NSE Stock Symbol (e.g., ITC.NS, TCS.NS, RELIANCE.NS)", "ITC.NS")

period = st.selectbox(
    "Select Time Period",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y"]
)

# ----------------------------
# FETCH DATA
# ----------------------------
st.subheader("Fetching Data...")

try:
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
except:
    st.error("Error loading stock data. Check the symbol.")
    st.stop()

if data.empty:
    st.error("No data found for this stock.")
    st.stop()

# ----------------------------
# DISPLAY CHART
# ----------------------------
st.subheader("Price Chart")

st.line_chart(data["Close"])

# ----------------------------
# MOVING AVERAGES
# ----------------------------
st.subheader("Moving Averages (MA)")

data["MA20"] = data["Close"].rolling(20).mean()
data["MA50"] = data["Close"].rolling(50).mean()
data["MA200"] = data["Close"].rolling(200).mean()

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(data["Close"], label="Close Price")
ax.plot(data["MA20"], label="20-Day MA")
ax.plot(data["MA50"], label="50-Day MA")
ax.plot(data["MA200"], label="200-Day MA")
ax.legend()
st.pyplot(fig)

# ----------------------------
# FUNDAMENTALS SECTION
# ----------------------------
st.subheader("Fundamental Data")

info = stock.info

fundamentals = {
    "Company": info.get("longName", "N/A"),
    "Sector": info.get("sector", "N/A"),
    "Industry": info.get("industry", "N/A"),
    "Market Cap": info.get("marketCap", "N/A"),
    "PE Ratio": info.get("trailingPE", "N/A"),
    "PB Ratio": info.get("priceToBook", "N/A"),
    "52 Week High": info.get("fiftyTwoWeekHigh", "N/A"),
    "52 Week Low": info.get("fiftyTwoWeekLow", "N/A"),
}

st.table(pd.DataFrame(fundamentals.items(), columns=["Metric", "Value"]))

# ----------------------------
# RETURNS CALCULATOR
# ----------------------------
st.subheader("Returns Calculator")

returns = {}

if len(data) > 0:
    returns["1 Day"] = (data["Close"][-1] / data["Close"][-2] - 1) * 100 if len(data) > 1 else 0
    returns["1 Week"] = (data["Close"][-1] / data["Close"][-5] - 1) * 100 if len(data) > 5 else 0
    returns["1 Month"] = (data["Close"][-1] / data["Close"][-22] - 1) * 100 if len(data) > 22 else 0

st.table(pd.DataFrame(returns.items(), columns=["Period", "Return (%)"]))

# ----------------------------
# VOLUME ANALYSIS
# ----------------------------
st.subheader("Volume Trend")

fig2, ax2 = plt.subplots(figsize=(12, 4))
ax2.bar(data.index, data["Volume"])
ax2.set_title("Volume Over Time")
st.pyplot(fig2)

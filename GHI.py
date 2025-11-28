import streamlit as st
import yfinance as yf
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Trend Analyzer", layout="wide")

st.title("📈 Stock Trend Analyzer (ARIMA Prediction)")

# -------------------------------
# User Inputs
# -------------------------------
stock = st.text_input("Enter Stock Ticker (Example: TCS.NS, INFY.NS, ITC.NS)", "ITC.NS")
period = st.selectbox("Select Time Period", ["1y", "2y", "5y", "10y"])
forecast_days = st.slider("Forecast Days", 5, 60, 15)

# -------------------------------
# Fetch Data
# -------------------------------
st.subheader("Fetching Stock Data...")
data = yf.download(stock, period=period, interval="1d")

if data.empty:
    st.error("Invalid stock symbol or data unavailable")
    st.stop()

close_prices = data["Close"]

st.line_chart(close_prices)

# -------------------------------
# Prepare Model
# -------------------------------
st.subheader("Training ARIMA Model...")

try:
    model = ARIMA(close_prices, order=(5,1,2))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=forecast_days)
except:
    st.error("Model training failed. Try different stock or period.")
    st.stop()

# -------------------------------
# Plot Forecast
# -------------------------------
st.subheader(f"Forecast for next {forecast_days} days")

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(close_prices.index, close_prices, label="Actual Price")
ax.plot(pd.date_range(start=close_prices.index[-1], periods=forecast_days+1, closed='right'),
        forecast, label="Forecasted Price")
ax.set_title(f"{stock} Price Prediction")
ax.legend()
st.pyplot(fig)

# -------------------------------
# Final Dataframe
# -------------------------------
forecast_df = pd.DataFrame({
    "Date": pd.date_range(start=close_prices.index[-1], periods=forecast_days+1, closed='right'),
    "Predicted Price": forecast.values
})

st.subheader("Predicted Values")
st.dataframe(forecast_df)

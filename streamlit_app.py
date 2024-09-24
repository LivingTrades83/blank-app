import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

# Function to determine if a ticker is an ETF
def is_etf(ticker):
    # Add logic to decide if the ticker is an ETF or a regular stock
    # For example, you might query an API, or check a local list of ETFs
    # Here we implement a simple check; you can enhance the logic later
    etf_list = ['SPY', 'VOO', 'IVV', 'QQQ']  # Add more common ETF tickers
    return ticker in etf_list

# Function to fetch dividend data based on ticker type
def get_dividend_data(ticker):
    if is_etf(ticker):
        url = f"https://www.stockanalysis.com/etfs/{ticker}/dividend/"
    else:
        url = f"https://www.stockanalysis.com/stocks/{ticker}/dividend/"

    response = requests.get(url)
    if response.status_code != 200:
        st.error(f"Failed to fetch data for {ticker} from stockanalysis.com")
        return None

    data = pd.read_html(response.text)
    return data[0]  # Assuming the dividend data is the first table

# Function to analyze stock performance
def analyze_data(data):
    return data.describe()

# Streamlit app
st.title("Dividend Data Analyzer")

tickers_input = st.text_input("Enter stock tickers (comma separated):")
tickers = [ticker.strip() for ticker in tickers_input.split(',') if ticker.strip()]

if st.button('Get Dividend Data'):
    for ticker in tickers:
        st.subheader(f"Ticker: {ticker}")
        dividend_data = get_dividend_data(ticker)

        if dividend_data is not None:
            st.write(dividend_data)  # Display the full DataFrame for debugging

            # Check the columns
            st.write("Columns in the DataFrame:", dividend_data.columns.tolist())

            # Make sure to adjust the names as per the actual column names
            # Assuming the first column is the date and the second is the dividend
            # You would check/rename here based on the actual data structure
            if 'Date' in dividend_data.columns and 'Dividend' in dividend_data.columns:
                # Create charts
                sns.set(style='whitegrid')
                plt.figure(figsize=(10, 5))
                sns.lineplot(data=dividend_data, x='Pay Date', y='Cash Amount', marker='o')
                plt.title(f'{ticker} Dividend Over Time')
                plt.xlabel("Date")
                plt.ylabel("Dividend Amount")
                plt.xticks(rotation=45)
                st.pyplot(plt)
            else:
                st.error("Expected 'Date' and 'Dividend' columns not found in data.")
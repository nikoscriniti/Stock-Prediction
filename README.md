# Stock Predictor

Stock Predictor is a web-based application built with Streamlit that allows users to analyze stock market data and make predictions using historical stock prices. It uses the Prophet library for forecasting and Plotly for data visualization.



# Data
- comes from yahoo finance for the data

# UI
- streamlit
1. benefits: shows you erros in why your code is not outputing

# Predictor
- facebook profit
- - https://facebook.github.io/prophet/docs/installation.html
 -  - Algorthim written by facebook (avalible in R and python)


# graph system
- ploty

# steps to setup project
- create virtual environment: python3 -m venv stockprediction
- go to virtual environemnt: source stockprediction/bin/activate 
- download dependencies: pip3 install -r dependencies.txt
1. streamlit
2. prophet 
3. yfinance
4. plotly

# How to Use
Select a stock

Use the dropdown menu to choose a stock from a list of companies (e.g., AAPL, GOOG, TSLA).
Set the prediction period

Use the slider to select the number of years (1 to 4) for which you want to predict stock prices.
View raw data

The application will load and display the most recent historical data for the selected stock.
Visualize stock data

See time series plots of the stock's opening and closing prices.
View an interactive candlestick chart for a more detailed analysis.
Forecast future stock prices

The app uses Prophet to predict future stock prices. The forecast data and components (trend, seasonality) are displayed.
Download forecast data

Download the forecasted data as a CSV file for further analysis.


# pandas 
- Pandas DataFrame like a table in Excel. It has rows and columns, where each column is like a list of data, and each row is a data entry. You can easily do things like sorting, filtering, or finding averages, making it a great tool for working with data in Python.

# dataframe
- A data frame is a two-dimensional data structure, like a table with rows and columns. It is commonly used in data analysis tools like Pandas in Python or R. Each column can store different types of data (e.g., numbers, text), and each row represents an observation or record. Data frames allow for easy manipulation, analysis, and visualization of structured data.

# why CACHE
- Caching the data means storing a copy of the data in a temporary storage location so it can be accessed more quickly the next time it's needed. Instead of fetching or computing the data again from the original source (which could be slow), the program retrieves the cached copy, speeding up performance.



# News API
-- used: https://www.marketaux.com/account/dashboard
-- documentation: https://www.marketaux.com/documentation
-- REMEMBER: API Usage
            Available - 100
            Used - 0
            Remaining - 100

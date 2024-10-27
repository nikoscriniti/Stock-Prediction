# to run: streamlit run main.py
import streamlit as st
from datetime import date

import yfinance as yf
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objects as go
import requests # for news api

api_token = ""  #api token for news system, from https://www.marketaux.com/account/dashboard


START = "2016-01-01"
TODAY = date.today().strftime("%Y-%m-%d") # give us the current day in this format
#.strftime() --> the arugment is how we want it to look 

st.title("Stock Predictor")

# different choices:
'''put in the different stock names'''
stocks = ("AAPL", "GOOG", "MSFT", "GME", 
          "TSLA", "AMZN", "FB", "NFLX", 
          "NVDA", "INTC", "AMD", "BA", 
          "DIS", "JPM", "V", "WMT", "JNJ", 
          "KO", "NKE", "BABA")
selected_stock = st.selectbox("SELECT DATASET", stocks)

# slider for number of years for prediction
n_years = st.slider("YEARS OF PREDICTION", 1, 6) # start and end value (1, 4)
period = n_years * 365



#------------------------------------------#
#use a dectorator to cache the data... 
@st.cache  
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    # downloads all the data from START to TODAY date
    data.reset_index(inplace=True) # inplace=True will put the date in the very first coloum of the pandas dataframe
    return data

data_load_state = st.text("load data...")
data = load_data(selected_stock)
data_load_state.text("Loading data.... done")#reset text when the two options are done, above
#------------------------------------------#
st.subheader('Raw data') # look at the raw panadas dataframe
st.write(data.tail()) # pandas dataframe that streamlit can handle (we want to get the tail end of the dataframe so use tail)


def plot_raw_data():
    fig = go.Figure() 
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))# add trace 
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
    fig.layout.update(title_text="TIME SERIES DATA", xaxis_rangeslider_visible=True) # to get the title:xaxis_rangeslider_visible=True
    st.plotly_chart(fig) # plot using streamlit

plot_raw_data()


#****************************************************************#
# * FORECAST CODE * #
#- passing in data from yahoo fiance to be trained on alogirthm (fbprophet) 
#------------------------------------------#
'''forcasting with the facebook prophet'''
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"}) # this is how fbprophet nees it to look, ds and y (find this in Documentation on website)
    # ^^^ have to write it in a different way becaseu fbprophet expects it in different format

m = Prophet()
m.fit(df_train) # use dataframe train, it start the training 
future = m.make_future_dataframe(periods=period) # has to be in days 
forecast = m.predict(future) # predicting future dataframe

st.subheader('Forecast data') 
st.write(forecast.tail())  # last 10 rows (tail)
#------------------------------------------#

'''plotting the forecast data below'''
#use plotly function
st.write('forecast data')
fig1 = plot_plotly(m, forecast) #m = model
st.plotly_chart(fig1)

st.write('forecast components')
#using a normal graph
fig2 = m.plot_components(forecast) # NOT A PLOTLY CHART
st.write(fig2) # NOT A PLOTLY CHART

#------------------------------------------#
#download button
@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(forecast)

st.download_button(
    label="Download forecast data as CSV",
    data=csv,
    file_name='forecast_data.csv',
    mime='text/csv',
)
#------------------------------------------#
#****************************************************************#

'''NEW FEATURES'''
#------------------------------------------#
# Candlestick chart for historical data
def plot_candlestick():
    fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'])])
    fig.layout.update(title_text="Candlestick Chart", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
plot_candlestick()


# Calculate daily percentage change
data['Daily Change %'] = data['Close'].pct_change() * 100

# Plot daily percentage change
def plot_daily_change():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Daily Change %'], name='Daily % Change'))
    fig.layout.update(title_text="Daily Percentage Change", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_daily_change()

#Include volume analysis by plotting the trading volume over time.
def plot_volume_data():
    fig = go.Figure()
    fig.add_trace(go.Bar(x=data['Date'], y=data['Volume'], name='Volume'))
    fig.layout.update(title_text="Trading Volume Over Time", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_volume_data()


def fetch_news(api_token, symbol, language="en", limit=5):
    url = "https://api.marketaux.com/v1/news/all"
    params = {
        "api_token": api_token,
        "symbols": symbol,
        "language": language,
        "limit": limit,
        "filter_entities": "true"
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        st.error(f"Failed to fetch news: {response.json().get('error', {}).get('message', 'Unknown error')}")
        return []
    
    # Display news related to the selected stock
st.subheader(f"Latest News for {selected_stock}")
news_articles = fetch_news(api_token, selected_stock)

if news_articles:
    for article in news_articles:
        st.write(f"**{article['title']}**")
        st.write(article["description"])
        st.write(f"[Read more]({article['url']})")
        st.write(f"Published on: {article['published_at']}")
        st.write("---")
else:
    st.write("No news available for this stock.")
#------------------------------------------#



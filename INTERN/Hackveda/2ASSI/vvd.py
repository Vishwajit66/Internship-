import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go

START = "2015-1-24"
TODAY = date.today().strftime("%Y-%m-%d")

st.title("Stock Screener Application")

stocks = ("AAPL", "GOOG", "MSFT", "GME", "PLTR", "NVDA")
selected_stocks = st.selectbox("Select dataset for prediction", stocks)
n_years = st.slider("Years of prediction:", 1, 4)
period = n_years * 365

@st.cache_resource
def load_data(ticker):
    try:
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None
data_load_state = st.text("Loading data...")
data = load_data(selected_stocks)
if data is not None:
    data_load_state.text("Loading data...done!")
    
    st.subheader('Raw data')
    st.write(data.tail())

    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
        fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)
    
    plot_raw_data()

    # Forecasting
    df_train = data[['Date', 'Close']].dropna()
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    if df_train.shape[0] < 2:
        st.error("Insufficient data for forecasting. Dataframe has less than 2 non-NaN rows.")
    else:
        m = Prophet()
        m.fit(df_train)
        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)

        st.subheader('Forecast data')
        st.write(forecast.tail())

        st.write('Forecast data')
        fig1 = plot_plotly(m, forecast)
        st.plotly_chart(fig1)

        st.write('Forecast components')
        fig2 = m.plot_components(forecast)
        st.write(fig2)
else:
    st.error("Failed to load data. Please check your internet connection or try again later.")

import yfinance as yf
import pandas as pd
import streamlit as st
import datetime
from pathlib import Path
from gmail.email_sender import send_email

def fetch_periods_intervals():
    return [
        "1d",
        "5d",
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "10y",
        "ytd",
        "max",
    ]


def get_stocks():
    path = Path.cwd() / "data" / "all_stocks.txt"
    with open(path) as f:
        stocks = f.read().splitlines()
    return stocks


def generate_analysis_excel(all_stocks, selected_stocks, history_period, email_to, key):
    if (len(selected_stocks) == 0):
        selected_stocks = all_stocks
    data = []
    error_stocks = []
    for stock_code in selected_stocks:
        print("Analying " + stock_code)
        link = f'=HYPERLINK("https://finance.yahoo.com/quote/{stock_code}?.tsrc=fin-srch")'

        try:
            stock = yf.Ticker(stock_code)
            value = get_info_data_or_default('currentPrice', stock.info)
            review = get_info_data_or_default('recommendationKey', stock.info)
            sector = get_info_data_or_default('sector', stock.info)
            dividend_date = get_info_data_or_default('exDividendDate', stock.info)
            country = get_info_data_or_default('country', stock.info)
            if dividend_date is not None and dividend_date is not "-":
                dividend_date = datetime.datetime.fromtimestamp(dividend_date).strftime('%Y-%m-%d %H:%M:%S')

            # historic
            historic_data = yf.download(stock_code, period=history_period)
            max = round(historic_data['High'].max(), 2)
            min = round(historic_data['Low'].min(), 2)
            var = max - min

            data.append([stock_code, value, review, sector, country, max, min, var, dividend_date, link, '', ''])
        except Exception as e:
            print("Cannot fetch data of " + stock_code)
            print(e)
            data.append([stock_code, "-", "-", "-", "-", "-", "-", "-", "-", link, '', ''])
            error_stocks.append(stock_code)

    df = pd.DataFrame(data, columns=['Stock', 'Value', 'Review', 'Sector', 'Country', 'Max', 'Min', 'Variation',
                                     'Dividends Date', 'Link', 'Chofa', 'Fede'])

    now = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    filename = Path.cwd() / "data" / f'StockAnalysis_{now}.xlsx'

    df.to_excel(filename)

    send_email(email_to, key, filename)

    if len(error_stocks) > 0:
        st.error("The following stocks cound not be analyzed: " + ", ".join(s for s in error_stocks))


def get_info_data_or_default(key, info):
    return info[key] if key in info.keys() else "-"

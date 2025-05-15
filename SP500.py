import pandas as pd
import requests
import yfinance as yf
import time
from numba import njit
import lxml

# Get the list of S&P 500 companies from Wikipedia
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

html = requests.get(url).content
df_list = pd.read_html(html)
df = df_list[0]

# Extract the ticker symbols
tickers = df['Symbol'].tolist()

# Create lists to store the ticker symbols and their sectors
share = []
sectors = []
PER=[]
ROA=[]
ROE=[]
REC=[]
EPS=[]

# Retrieve sector information using yfinance

for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        sector = info.get("sector", "Unknown")
        PE=info.get("forwardPE", "Unknown")
        RoA=info.get("returnOnAssets","Unknown")
        RoE=info.get("returnOnEquity","Unknown")
        RECON=info.get("recommendationKey","Unknown")
        Eps=info.get("forwardEps", "Unknow")
        print(f"Sector of {ticker}: {sector}")
        time.sleep(1)
    except Exception as e:
        sector = "Unknown"
        print(f"Could not retrieve data for {ticker}: {e}")

    share.append(ticker)
    sectors.append(sector)
    PER.append(PE)
    ROA.append(RoA)
    ROE.append(RoE)
    REC.append(RECON)
    EPS.append(Eps)
    data = pd.DataFrame({'Symbol': share, 'Sector': sectors,'PER':PER,'ROA':ROA, 'ROE':ROE, 'REC':REC, 'EPS':EPS})
    data.to_csv("S&P500.csv")

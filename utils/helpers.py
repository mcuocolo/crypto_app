import pandas as pd
import requests
import streamlit as st

from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

cache_deprecation = 120

# call 100 top currency by market cap

@st.cache_data(ttl=cache_deprecation)
def get_dataframe(vs="usd"):
    data = cg.get_coins_markets(vs_currency=vs, order="market_cap_desc", 
                            price_change_percentage="1h,24h,7d")
    
    #A function that returns the html code as it should
    def show_image_from_url(image_url):
        return(f"st.image({image_url})")
    
    df = pd.DataFrame(data)
    df = df.set_index("symbol")
    cols = ["name", "small_image", "current_price", "total_volume",
       "high_24h", "low_24h", "price_change_24h",
       "price_change_percentage_24h",
       "last_updated",
       "price_change_percentage_1h_in_currency",
       "price_change_percentage_24h_in_currency",
       "price_change_percentage_7d_in_currency"]
    df["small_image"] = df["image"]
    df.last_updated = pd.to_datetime(df.last_updated).dt.strftime('%B %d %Y - %r %Z')
    df = df[cols].rename(columns={"name":"Name",
                                  "small_image": "Image",
                                  "current_price":"Price", 
                                  "total_volume":"Volume",
                                  "high_24h":"High", 
                                  "low_24h":"Low", 
                                  "price_change_percentage_1h_in_currency":"1h",
                                  "price_change_percentage_24h_in_currency":"24h",
                                  "price_change_percentage_7d_in_currency":"7d"})
    return df

@st.cache_data(ttl=cache_deprecation)
def get_trending():
    data = cg.get_search_trending()["coins"]
    # create and return lists
    names = []
    img_thumb = []
    price_btc = []
    market_cap_rank = []
    for i in range(len(data)):
        names.append(data[i]["item"]["name"])
        market_cap_rank.append(data[i]["item"]["market_cap_rank"])
        img_thumb.append(data[i]["item"]["thumb"])
        price_btc.append(data[i]["item"]["price_btc"])
    return names, market_cap_rank, img_thumb, price_btc

@st.cache_data(ttl=cache_deprecation)
def get_btc_price():
    """ return btc price as float for conversion calculations"""
    btc_price = cg.get_price(ids="bitcoin", vs_currencies="usd")
    return float(btc_price["bitcoin"]["usd"])

@st.cache_data(ttl=cache_deprecation)
def get_price(coin):
    """ return coin price for metrics """
    coin_data = cg.get_coins_markets(ids=coin, vs_currency="usd")
    price = f"{float(coin_data[0]['current_price']):_.2f}".replace("_","'")
    pct_change_24h = f"{round(float(coin_data[0]['price_change_percentage_24h']),2)} %"
    img = coin_data[0]['image']
    return price, pct_change_24h, img

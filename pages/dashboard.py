import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from utils.helpers import get_dataframe, get_trending, get_btc_price, get_price

COLOR = 'white'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR
mpl.rcParams['figure.facecolor'] = "black"
mpl.rcParams['axes.facecolor'] = "black"
mpl.rcParams["figure.dpi"] = 100

# set page to full screen
icon = Image.open("images/bitcoin.ico")
st.set_page_config(page_title="Custom crypto app",
                   page_icon=icon,
                   layout="wide")   

# specifying left and right columns to add some "margins" while keeping wide layout
margin_left, cola, colb, margin_right = st.columns([1, 3, 3, 1])

with cola:
    st.title("Crypto Price Dashboard")
    st.image("images/bitcoin.webp")
    st.markdown("""
    This app retrieves prices for the top 100 cryptocurrencies by market capitalization from Coingecko.
    """)

    pix1, col1, pix2, col2, pix3, col3 = st.columns([1, 3, 1, 3, 1, 3])
    coins_list = ["bitcoin", "ethereum", "binancecoin"]
    coins_data = []
    for coin in coins_list:
        coins_data.append(get_price(coin))

    with pix1:
        st.image(coins_data[0][2], width=50)
    with col1:
        st.metric(label=coins_list[0], value=coins_data[0][0], delta=coins_data[0][1])
    with pix2:
        st.image(coins_data[1][2], width=50)
    with col2:
        st.metric(label=coins_list[1], value=coins_data[1][0], delta=coins_data[1][1])
    with pix3:
        st.image(coins_data[2][2], width=50)
    with col3:
        st.metric(label=coins_list[2], value=coins_data[2][0], delta=coins_data[2][1])

    st.header("Input options")
    currency_price_unit = st.selectbox("Select base currency", 
                                       options=["USD", "BTC", "ETH"])
    
    df = get_dataframe(currency_price_unit.lower())
    coin_list = st.multiselect("Choose among 100 top market cap urrencies", df.index)

    cols = ["Name", "Price", "Volume", "High", "Low", "1h", "24h" ,"7d"]
    df_small = df[cols]
    st.dataframe(df_small.loc[coin_list]) 

    st.write(f"Data last updated : {df.last_updated[0]}")
    with st.expander("About"):
        st.markdown("""
        * **Python libraries :** streamlit, Pillow, pandas, matplotlib, pycoingecko
        * **Data source :** [Coingecko](https://www.coingecko.com/)
        * **Credit :** Chanin Nantasenamat in Build 12 Data Science Apps with Python and Streamlit - [Full Course](https://https://www.youtube.com/watch?v=JwSS70SZdyM)
        * **Credit also :** Myself as tutorial is mostly outdated and code needs to be significantly modified in order to work. But idea is quite cool anyway...
        Replaced BeautifulSoup with coingecko API calls using pycoingecko wrapper.
    """)  


with colb:   
    st.subheader("Top 7 trending in coingecko")
    names, market_cap_rank, img_thumb, price_btc = get_trending()
    btc_usd = get_btc_price()
    colimg, colnames, colmkt, colprice = st.columns(4)
    with colimg:
        st.markdown("**Icon**")
        for i in range(7):
            st.image(img_thumb[i])
    with colnames:
        st.markdown("**Coin**")
        for i in range(7):
            st.write(names[i])
    with colmkt:
        st.markdown("**Market cap rank**")
        for i in range(7):
            st.write(market_cap_rank[i])
    with colprice:
        st.markdown("**Price (USD)**")
        for i in range(7):
            price_usd = float(price_btc[i]) * btc_usd
            st.write(round(price_usd, 4))


    period_choice = st.selectbox("Period", ["1h", "24h" ,"7d"])
    if coin_list != []:
        st.subheader(f"Selected coins {period_choice} %")
        df_sorted = df.loc[coin_list].sort_values(by=period_choice, ascending=False)
        df_sorted["positive"] = df_sorted[period_choice] > 0
        plt.figure(figsize=(5, 5))
        df_sorted[period_choice].plot(kind="barh", color=df_sorted.positive.map({True: "g", False: "r"}))
        st.pyplot(plt)










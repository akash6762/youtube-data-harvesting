import json

import requests
import streamlit as st
from streamlit_option_menu import option_menu

from css_js import css_js_for_whole_app

# page configurations
st.set_page_config(
    page_title = "youtube data", 
    page_icon = ":bar_chart:"
)


# load lottie gifs with file path
def display_lottie_with_path(path: str):
    with open(path, "r") as file:
        return json.load(file)

# load lottie gif with url 
def display_lottie_with_url(url: str):
    request = requests.get(url)
    if request.status_code != 200:
        return None
    else:
        return request.json()
    

# sidebar 
with st.sidebar:
    selected = option_menu(
        menu_title = None, 
        options= ["Home", "Scraper", "Analytics", "Help"], 
        icons = ["house", "youtube", "bar-chart-fill",  "question-circle-fill"]
    )
    
# custum css
st.markdown(css_js_for_whole_app, unsafe_allow_html=True)


if selected == "Home":
    
    # YouTube scraper image
    st.image("/home/akash/D/projects/youtube/media/photos/youtube.png", caption = None)
    st.markdown("""
    
                <p class="paragraph"> Welcome to our YouTube Data Harvesting and Warehousing app! Our app is designed to simplify the process of gathering and storing valuable data from YouTube channels and videos, empowering you with powerful insights and analytics.
Whether you're a content creator, marketer, researcher, or simply curious about YouTube data, our app provides you with an efficient and intuitive solution. With just a few clicks, you can retrieve comprehensive information about channels, videos, views, likes, comments, and more.
Harnessing the power of the YouTube Data API, our app allows you to enter the channel ID or channel name of your choice and access a wealth of data. We handle the retrieval process seamlessly, ensuring you get the most up-to-date information available.</p>

<p class="paragraph"> But we don't stop at data retrieval. Our app also offers sophisticated data warehousing capabilities. You can securely store the collected data in a centralized database, enabling you to analyze trends, identify patterns, and gain valuable insights. Leverage our search and query functionality to find specific videos, track engagement metrics, and make informed decisions to optimize your YouTube strategies. </p>
<p class="paragraph"> We're committed to providing you with a seamless user experience, intuitive navigation, and powerful features. Our app is continuously updated and improved based on user feedback and emerging trends in YouTube analytics.
Are you ready to unlock the potential of YouTube data? Get started with our app today and discover a whole new level of insights and opportunities. Start harvesting data, uncover trends, and make data-driven decisions to supercharge your YouTube presence. </p>
                """, 
                unsafe_allow_html=True)

if selected == "Scraper":
    st.markdown("""
                <h1> SCRAPER </h1>
                
                """,
                unsafe_allow_html=True)
    left_column, right_column = st.columns(2)
    with right_column:
        options = ["channel id", "channel name"]
        default = 0
        name_or_id_select = st.selectbox(
            "select an option", 
            options, 
            default
        ) 
        
    with left_column:
        if name_or_id_select == "channel id":
            channel_name_or_id = st.text_input("Enter channel id")
        if name_or_id_select == "channel name":
            channel_name_or_id = st.text_input("Enter channel name")
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    execute = st.button("Execute")

if selected == "Analytics":
    st.markdown("""
                <h1> Youtube Analytics </h1>
                """, 
                unsafe_allow_html=True)
    
if selected == "Help":
    st.header("Help")
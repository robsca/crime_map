import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
import geocoder
import streamlit as st

st.set_page_config(layout="wide")
st.title('London police: Crime Data')

# Input
address_ = st.sidebar.text_input('Insert adress')

# Find location
geolocator = Nominatim(user_agent="run.py") #name of the file
location = geolocator.geocode(str(address_))

# Show results 
if st.button('Press'):
try:
    # Create map
    address = location.address
    column1, column2 = st.columns(2)
    with column1:
        # plot map crime density
        from get_map_plot import get_data_and_plot
        a = get_data_and_plot(location.latitude, location.longitude)
    with column2:
        # get categories - pie chart
        from get_categories_piechart import categories
        cat = categories(location.latitude, location.longitude)
except:
    st.subheader('Select a valid location')

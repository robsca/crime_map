import streamlit as st
st.set_page_config(layout="wide")

import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
import geocoder
from police_api import PoliceAPI
api = PoliceAPI()
import plotly.express as px
import numpy
import pydeck as pdk
import pandas as pd


def categories(lat,lng):    
    '''
    This function takes a latitude and longitude and returns a pie chart with the categories of crimes that happened in that area
    '''
    crimes = api.get_crimes_point(lat, lng, date=None, category=None)

    '''Find the category of every crime and put in a list'''
    crimes_type = []
    for crime in crimes:
        category = crime.category
        crimes_type.append(category)
    #print(crimes_type)
    '''Find how many different categories there are in the array, and create a list with all of them'''
    categories = list(dict.fromkeys(crimes_type))
    categories_list = []
    for category in categories:
        categ = str(category)
        c = categ.split()
        c = c[1:]
        categories_list.append(c)
    #print(categories_list)
    '''Transform the first array and prepare it for counting'''
    crimes_ = []
    for crime_type in crimes_type:
        crime_type = str(crime_type)
        c = crime_type.split()
        c = c[1:]
        crimes_.append(c)
    '''Count how many episode of each category occure in that date range'''
    ranking = []
    for cat in categories_list:
        counter = crimes_.count(cat)
        ranking.append([cat, counter])

    #plot result
    labels = [' '.join(ranking[i][0]) for i in range(len(ranking))]
    values = [ranking[i][1] for i in range(len(ranking))]

    
    fig = px.pie(values=values, names=labels)
    st.plotly_chart(fig)

def get_data_and_plot(lat,lng):
    crimes = api.get_crimes_point(lat, lng, date=None, category=None)

    lngs = []
    lats = []
    crimes_type = []
    for crime in crimes:
        location = crime.location
        lng = location.longitude
        lngs.append(float(lng))
        lat = location.latitude
        lats.append(float(lat))
        category = crime.category
        crimes_type.append(category)

    lats = np.array(lats)
    lngs = np.array(lngs)
    lats = lats.reshape(-1,)
    lngs = lngs.reshape(-1,)

    df = pd.DataFrame({'lon':lngs, 'lat': lats})

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=51.540046,
            longitude=-0.116655,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=df,
                get_position=['lon','lat'],
                radius=10,
                elevation_scale=3,
                elevation_range=[0, 100],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position=['lon','lat'],
                get_color='[200, 30, 0, 160]',
                get_radius=10,
            ),
        ],
    ))

def RunSearch(location):
    try:
        # Create map
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
        st.subheader("Select a valid location")
        st.subheader("Make sure you put the space in the right spot - ex. N1 1BB")

st.title('London Police: Crime Data')

# Input
address_ = st.sidebar.text_input('Insert a Uk Postcode')
geolocator = Nominatim(user_agent="run.py") #name of the file
location = geolocator.geocode(str(address_))
# Button
search_button = st.sidebar.button('Search', on_click=RunSearch, args=(location,))
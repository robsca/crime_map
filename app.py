import streamlit as st
st.set_page_config(layout="wide")

import pandas as pd
from geopy.geocoders import Nominatim
import plotly.express as px

from police_api import PoliceAPI
api = PoliceAPI()
boroughs_of_london = {
      'Barking and Dagenham': [51.5607, 0.1557], # 32 full
      'Barnet': [51.6252, -0.1517], # 31 full
      'Bexley': [51.4549, 0.1505], # 30 full
      'Brent': [51.5588, -0.2817], # 29 full
      'Bromley': [51.4039, 0.0198], # full
      'Camden': [51.5290, -0.1255], #full
      'City of London': [51.5155, -0.0922],
      'Croydon': [51.3714, -0.0977], 
      'Ealing': [51.5130, -0.3089], 
      'Enfield': [51.6538, -0.0799],
      'Greenwich': [51.4892, 0.0648],
      'Hackney': [51.5450, -0.0553], 
      'Hammersmith and Fulham': [51.4927, -0.2240], 
      'Haringey': [51.6024, -0.0940], 
      'Harrow': [51.5898, -0.3346], 
      'Havering': [51.5607, 0.1837], 
      'Hillingdon': [51.5471, -0.4714], 
      'Hounslow': [51.4746, -0.3630], 
      'Islington': [51.5416, -0.1022],
      'Kensington and Chelsea': [51.4973, -0.1947],
      'Kingston upon Thames': [51.4085, -0.3064],
      'Lambeth': [51.4607, -0.1162],
      'Lewisham': [51.4452, -0.0209],
      'Merton': [51.4014, -0.1958],
      'Newham': [51.5077, 0.0469],
      'Redbridge': [51.5590, 0.0741],
      'Richmond upon Thames': [51.4479, -0.3210],
      'Southwark': [51.5035, -0.0804],
      'Sutton': [51.3618, -0.1945],
      'Tower Hamlets': [51.5077, -0.0058],
      'Waltham Forest': [51.5908, -0.0134],
      'Wandsworth': [51.4567, -0.1910],
      'Westminster': [51.4973, -0.1372]
}
   
class API_Police:

   def __init__(self, postcode):
      self.api = PoliceAPI()
      self.postcode = postcode
      geolocator = Nominatim(user_agent="run.py") #name of the file
      self.location = geolocator.geocode(str(postcode))
      self.lat = self.location.latitude
      self.lng = self.location.longitude
      self.crimes = api.get_crimes_point(self.lat, self.lng)
      self.building_dataframe()

   def building_dataframe(self):
      self.crimes_ids = [crime.id for crime in self.crimes]
      self.crimes_categories = [crime.category.name for crime in self.crimes]
      self.crimes_dates = [crime.month for crime in self.crimes]
      self.crimes_locations = [crime for crime in self.crimes]
      self.crimes_lats = [crime.location.latitude for crime in self.crimes]
      self.crimes_lngs = [crime.location.longitude for crime in self.crimes]
      self.crimes_name_street = [crime.location.name for crime in self.crimes]
      self.crimes_outcomes = [crime.outcome_status if crime.outcome_status != None else 'None' for crime in self.crimes]
      # split at  > it it's there
      self.crimes_outcomes = [str(crime).split('>')[-1] for crime in self.crimes_outcomes]
      # replace no suspect identified by None
      self.crimes_outcomes = [crime.replace('no suspect identified', 'NSI').replace(";", "") for crime in self.crimes_outcomes]
      # take off On or near from the street name if it's there
      self.crimes_name_street = [crime.replace('On or near ', '') for crime in self.crimes_name_street]
      # take off empty spaces at the end of the street name
      frame = {'id': self.crimes_ids, 'category': self.crimes_categories, 'date': self.crimes_dates, 'lat': self.crimes_lats, 'lng': self.crimes_lngs, 'outcome': self.crimes_outcomes, 'street': self.crimes_name_street}
      self.df = pd.DataFrame(frame)
      self.df['date'] = pd.to_datetime(self.df['date']).dt.date
      # transform the lat and lng into floats
      self.df['lat'] = self.df['lat'].astype(float)
      self.df['lng'] = self.df['lng'].astype(float)

def graph_crimes_map(df):
   fig = px.scatter_mapbox(df, lat="lat", lon="lng", hover_name="street", hover_data=["category", "date", "outcome"], color="category", zoom=10, height=300)
   fig.update_layout(mapbox_style="carto-positron") # or "white-bg", "carto-positron", "carto-darkmatter"
   fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
   # update marker size and opacity and zoom
   fig.update_traces(marker=dict(size=10, opacity=0.5))
   fig.update_layout(mapbox_zoom=12, mapbox_center_lat = df['lat'].mean(), mapbox_center_lon = df['lng'].mean())
   
   # legend need to go somewhere else
   fig.update_layout(legend=dict(
      yanchor="top",
      y=0.99,

      xanchor="left",
      x=0.01
   ))

   st.plotly_chart(fig, use_container_width=True)

def graph_pie_chart(df):
   # count the number of crimes per category
   df = df.groupby('category').count().reset_index()
   fig = px.bar(df, x='category', y=df.columns[1], color='category')
   st.plotly_chart(fig, use_container_width=True)

def graph_outcome_pie_chart(df):
   fig = px.pie(df, values='id', names='outcome')
   fig.update_traces(textposition='inside', textinfo='percent+label')
   st.plotly_chart(fig, use_container_width=True)

def graph_street_count(df):
   df = df.groupby('street').count().reset_index()
   # sort by count
   df = df.sort_values(by=df.columns[1], ascending=False)
   # no empty streets
   df = df[df['street'] != '']
   df = df.head(10)
   fig = px.bar(df, x='street', y=df.columns[1], color='street')
   st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
   st.title("UK Crime Map")
   c1,c2 = st.columns(2)
   postcode = c1.text_input("Enter your postcode")
   boroughs_of_london_choices = list(boroughs_of_london.keys())+["None"]
   boroughs_of_london_input = c2.selectbox("Select your borough", boroughs_of_london_choices, index=0)
   
   if boroughs_of_london_input != "None":
      postcode = boroughs_of_london[boroughs_of_london_input]
   
   if postcode:
      johnny = API_Police(postcode)

      # basic plots
      st.write("Number of crimes in this month: ", str(len(johnny.df)))

      category_filter = st.sidebar.multiselect("Select the categories you want to see", johnny.df['category'].unique())
      street_filter = st.sidebar.multiselect("Select the streets you want to see", johnny.df['street'].unique())

      if category_filter:
         filtered = johnny.df[johnny.df['category'].isin(category_filter)]
      else:
         filtered = johnny.df

      if street_filter:
         filtered = filtered[filtered['street'].isin(street_filter)]
      else:
         filtered = filtered
      
      graph_street_count(filtered)
      graph_crimes_map(filtered)   
      c1,c2 = st.columns(2)
      with c1:
         graph_pie_chart(filtered)
      with c2:
         graph_outcome_pie_chart(filtered)


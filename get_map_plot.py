def get_data_and_plot(lat,lng):
    from police_api import PoliceAPI
    api = PoliceAPI()

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

    import numpy as np
    lats = np.array(lats)
    lngs = np.array(lngs)
    lats = lats.reshape(-1,)
    lngs = lngs.reshape(-1,)

    import pandas as pd
    #coordinates = pd.DataFrame({'lat':lats, 'lon':lngs})
    df = pd.DataFrame({'lon':lngs, 'lat': lats})

    import pydeck as pdk
    coords = ['lon','lat']
    import streamlit as st

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
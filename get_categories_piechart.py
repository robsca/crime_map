def categories(lat,lng):    
    from police_api import PoliceAPI
    api = PoliceAPI()
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
    import plotly.express as px
    import numpy
    
    fig = px.pie(values=values, names=labels)
    import streamlit as st
    st.plotly_chart(fig)
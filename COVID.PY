import numpy as np
import seaborn as sns
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt

st.title("COVID VACCINATION UPDATE")

def load_data():
    df_vaccines = pd.read_csv(r"https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv")
    return df_vaccines

df_vaccines = load_data()
print(df_vaccines)

#data cleaning and grouping

data = df_vaccines.loc[(df_vaccines["location"] != "World") & (df_vaccines["location"] != "Africa") & (df_vaccines["location"] != "Europe") & (df_vaccines["location"] != "Asia") & (df_vaccines["location"] != "Europian Union") & (df_vaccines["location"] != "North America") & (df_vaccines["location"] != "Northern Ireland") & (df_vaccines["location"] != "Northern Cyprus")]


#Data ko grouping on the basis of location and replace "NaN" values with zeros 

df_category = data[["location","date","total_vaccinations", "people_vaccinated","people_fully_vaccinated"]]
df_group = df_category.groupby("location")["location","date","total_vaccinations", "people_vaccinated","people_fully_vaccinated"].max()
df_result = pd.DataFrame(df_group).replace(np.NaN,0)

st.sidebar.checkbox("Show Analysis By Location",True,key=1)
country_select = st.sidebar.selectbox("Select a location",df_result['location'])
selected_country = df_result[df_result["location"]==country_select]

def get_vaccine_analysis(dataresult):
    total_res = pd.DataFrame({'Status': ['Total vaccination','People Vaccinated', 'People Fully vaccinated'], 'Figure': (dataresult.iloc[0]['total_vaccinations'], dataresult.iloc[0]['people_vaccinated'], dataresult.iloc[0]['people_fully_vaccinated'] )})
    return total_res


total_country = get_vaccine_analysis(selected_country)

st.markdown("## **location level analysis**")
location_total_vaccinations = total_country.Figure[0]
location_people_vaccinated = total_country.Figure[1]
location_people_fully_vaccinated = total_country.Figure[2]

col1, col2 = st.columns(2)
col1.text("Location")
col1.info(country_select)
col2.text("total vaccinations (Cummulative)")
col2.info(f"{location_total_vaccinations}")

col1, col2 = st.columns(2)
col1.text("No of People vaccinated (Cummulative)")
col2.info(f"{location_people_vaccinated:,}")
col2.text("No of People fully vaccinated (Cummulative)")
col2.info(f"{location_people_fully_vaccinated:,}")


if st.sidebar.checkbox("Show Analysis by Location",True,key=2):
    st.markdown("## **Location level analysis - Visualization**")
    st.markdown("### Total vaccinations , People Vaccinated and " + "People fully vaccinated in %s" % (country_select))
    if not st.checkbox('Hide Graph',False,key=3):
        state_total_graph = px.bar(
            total_country,
            x="Status",
            y="Figure",
            labels={'Figure':'Figure in %s' % (country_select)},
            color='Status'
        )
        st.plotly_chart(state_total_graph)
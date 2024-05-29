# Streamlit live coding script
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

# First some MPG Data Exploration
# mpg_df = pd.read_csv("./data/mpg.csv")


# Problem, takes a lot of memoy => in cache
# but should not touch original data => raw
# tehn copy raw and put it df

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

mpg_df_raw = load_data("./data/mpg.csv")  # for speed
mpg_df = deepcopy(mpg_df_raw) # for security


# Add title and header
st.title("Introduction to Streamlit")
st.header("MPG Data Exploration")

test = st.checkbox('test')
'test: ', test    # check to show what's going on

if st.checkbox("Show Dataframe"):

    st.subheader("This is my dataset:")   
    # st.table(data=mpg_df)   UGLY
    st.dataframe(data=mpg_df)  # prettier


# if you want to put somthing on teh side: sue if st.sidebar () 

#left_column, right_column = st.columns(2)
left_column, middle_column, right_column = st.columns([3, 1, 1]) # allows so specify the width of the columns

# make a dropdown menu to update plots
years = ["All"]+sorted(pd.unique(mpg_df['year']))
year = left_column.selectbox("Choose a Year", years)   # dropdown . by specfyng teh left column instead of st.selectbox, we put it on teh left

show_means = middle_column.radio(
    label='Show Class Means', options=['Yes', 'No'])  # this is a radio button

# so basically, st. is the base placement

plot_types = ["Matplotlib", "Plotly"]
plot_type = right_column.radio("Choose Plot Type", plot_types)

# st.write(show_means)

if year == "All":
    reduced_df = mpg_df
else:
    reduced_df = mpg_df[mpg_df["year"] == year]

means = reduced_df.groupby('class').mean(numeric_only=True)

m_fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(reduced_df['displ'], reduced_df['hwy'], alpha=0.7)
ax.set_title("Engine Size vs. Highway Fuel Mileage")
ax.set_xlabel('Displacement (Liters)')
ax.set_ylabel('MPG')

if show_means == "Yes":
    ax.scatter(means['displ'], means['hwy'], alpha=0.7,
               color="red", label="Class Means")

#st.pyplot(m_fig)

# In Plotly
p_fig = px.scatter(reduced_df, x='displ', y='hwy', opacity=0.5,
                   range_x=[1, 8], range_y=[10, 50],
                   width=750, height=600,
                   labels={"displ": "Displacement (Liters)",
                           "hwy": "MPG"},
                   title="Engine Size vs. Highway Fuel Mileage")
p_fig.update_layout(title_font_size=22)

if show_means == "Yes":
    p_fig.add_trace(go.Scatter(x=means['displ'], y=means['hwy'],
                               mode="markers"))
    p_fig.update_layout(showlegend=False)

#st.plotly_chart(p_fig)

if plot_type == "Matplotlib":
    st.pyplot(m_fig)
else:
    st.plotly_chart(p_fig)

# We can write stuff
url = "https://archive.ics.uci.edu/ml/datasets/auto+mpg"
st.write("Data Source:", url)
# "This works too:", url

# Sample Streamlit Map
st.subheader("Streamlit Map")
ds_geo = px.data.carshare()



ds_geo['lat'] = ds_geo['centroid_lat'] # streamlist automatically knows what to do with lat and lon
ds_geo['lon'] = ds_geo['centroid_lon']



st.map(ds_geo)

st.dataframe(ds_geo.head())




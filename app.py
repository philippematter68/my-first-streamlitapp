# Streamlit live coding script
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

with st.form(key='my_form'):
   username = st.text_input('Username')
   password = st.text_input('Password')
   st.form_submit_button('Login')

if (username != "un") | (password != 'pw'):
    st.stop()

# Add title and header
st.title("Introduction to Streamlit")
st.header("MPG Data Exploration")


# A Dataset, takes a lot of memory => in cache
# but should not touch original data => raw
# then copy raw and put it as a df


@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df



mpg_df_raw = load_data("./data/mpg.csv")  # for speed
mpg_df = deepcopy(mpg_df_raw) # for security

# warning, if this command is before the title, everything gets messed up !
left_column, middle_column, right_column = st.columns([2, 2, 2]) # allows to specify the width of the columns
# by specifying a column instead of st.write, st.radio.stcheckbox... , we put it on the correct spot.
### WArning, in this case the text gets added down SEPARETELY in each column! 

# check to show what's going on with a checkbox:
test = middle_column.checkbox('test: check me !')
right_column.write('Am I checked ? '+ str(test)) #, right_column.write(test)    If I write the variable test separetely, it gets on another line => put it in the same string

### resets here the alignement:  
left_column, middle_column, right_column = st.columns([2, 2, 2]) # allows to specify the width of the columns

# defines variables needed for later:
if st.sidebar.checkbox("Show Dataframe"): # put something on the side: use if st.sidebar.selectbox () # so basically, st. is the "base" placement, which can later be refined.
    st.subheader("This is my dataset:")   
    st.dataframe(data=mpg_df)  # prettier than st.table()

# make a dropdown menu to update plots
years = ["All"]+sorted(pd.unique(mpg_df['year']))
year = st.sidebar.selectbox("Choose a Year", years)   # dropdown . 
# add radio buttons to select options
show_means = st.sidebar.radio(label='Show Class Means', options=['Yes', 'No'])  
plot_types = ["Matplotlib", "Plotly"]
plot_type = st.sidebar.radio("Choose Plot Type", plot_types)  # can pass arguments as variables too !

# then get all variable results:
if year == "All":
    reduced_df = mpg_df
else:
    reduced_df = mpg_df[mpg_df["year"] == year]

means = reduced_df.groupby('class').mean(numeric_only=True)

# defines the different PLOTS:
# ######################### 
# In Matplotlib 
m_fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(reduced_df['displ'], reduced_df['hwy'], alpha=0.7)
ax.set_title("Engine Size vs. Highway Fuel Mileage")
ax.set_xlabel('Displacement (Liters)')
ax.set_ylabel('MPG')

if show_means == "Yes":    # in this case ADD another layer on the top:
    ax.scatter(means['displ'], means['hwy'], alpha=0.7,
               color="red", label="Class Means")


# In Plotly
p_fig = px.scatter(reduced_df, x='displ', y='hwy', opacity=0.5,
                   range_x=[1, 8], range_y=[10, 50],
                   width=750, height=600, 
                   labels={"displ": "Displacement (Liters)",
                           "hwy": "MPG"},
                   title="Engine Size vs. Highway Fuel Mileage")
p_fig.update_layout(title_font_size=22)

if show_means == "Yes":   # in this case ADD another trace:
    p_fig.add_trace(go.Scatter(x=means['displ'], y=means['hwy'],
                               mode="markers", marker=dict(color='red')))
    p_fig.update_layout(showlegend=False)


if plot_type == "Matplotlib":
    st.pyplot(m_fig)
else:
    st.plotly_chart(p_fig)

# We can write stuff
url = "https://archive.ics.uci.edu/ml/datasets/auto+mpg"
st.write("Data Source:", url)
"(this works too): Data Source ", url

# Sample Streamlit Map
st.subheader("Example of a Streamlit Map")
ds_geo = px.data.carshare()  # this is simply a sample data set



ds_geo['lat'] = ds_geo['centroid_lat'] # streamlist automatically knows what to do with lat and lon
ds_geo['lon'] = ds_geo['centroid_lon']

st.map(ds_geo) 

'and this is the original dataframe:'
st.dataframe(ds_geo.head())


st.image('./data/dolphin_trumpet.jpg',)

# Clear values from *all* in-memory or on-disk cached functions
# st.cache_data.clear()
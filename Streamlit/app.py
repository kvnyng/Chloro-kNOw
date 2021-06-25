from matplotlib.backends.backend_agg import RendererAgg
import streamlit as st
import numpy as np
import pandas as pd
import xmltodict
from pandas import json_normalize
import urllib.request
import seaborn as sns
import matplotlib
from matplotlib.figure import Figure
from PIL import Image
import gender_guesser.detector as gender
from streamlit_lottie import st_lottie
import requests

import matplotlib.pyplot as plt
import plotly.figure_factory as ff

from models.process_data import tokyoData, veniceData, newYorkData
st.set_page_config(layout="wide")

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# lottie_book = load_lottieurl('https://assets6.lottiefiles.com/packages/lf20_izy5ndvp.json')
# st_lottie(lottie_book, speed=1, height=200, key="initial")


matplotlib.use("agg")
_lock = RendererAgg.lock


sns.set_style('darkgrid')
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.beta_columns(
    (.1, 2, .2, 1, .1))

row0_1.title('Looking At The Bigger Picture')

with row0_2:
    st.write('')

row0_2.subheader(
    'Soulution by the [Nimbus Team](https://github.com/bykevinyang/Nimbus)')

row1_spacer1, row1_1, row1_spacer2 = st.beta_columns((.1, 3.2, .1))

with row1_1:
    st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

st.markdown("""---""")
st.write('')
row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.beta_columns(
    (.1, 1, .1, 1, .1))

with row3_1, _lock:
    st.subheader("Tokyo Data")

    # Load Tokyo data.
    @st.cache(allow_output_mutation=True)
    def load_data():
        return  tokyoData()
    data_load_state = st.text('Loading data...')
    chl_df_tokyo = load_data()
    data_load_state.text('')
    st.dataframe(chl_df_tokyo)
    year_to_filter = st.slider('Filter years', 2019, 2021, 2021, key='tokyo')  # min: 0h, max: 23h, default: 17h

    # st.markdown("Looks like the average publication date is around **{}**, with your oldest book being **{}** and your youngest being ****.")
    # st.markdown("Note that the publication date on Goodreads is the **last** publication date, so the data is altered for any book that has been republished by a publisher.")


with row3_2, _lock:
    st.subheader("Plot of Tokyo's Data")
    @st.cache(allow_output_mutation=True)
    def load_data():
        return  tokyoData()
    data_load_state = st.text('Loading data...')
    chl_df_tokyo = load_data()
    data_load_state.text('')
    chl_df_tokyo.sort_values(by='Time', ascending=True, inplace=True)
    chl_df_tokyo['time'] = pd.to_datetime(chl_df_tokyo.Time)
    chl_df_tokyo = chl_df_tokyo[chl_df_tokyo['time'].dt.year == year_to_filter]

    fig = Figure()
    ax = fig.subplots()
    # plt.figure(figsize=(15, 15))

    ax.plot(chl_df_tokyo['Time'], chl_df_tokyo['Chl_concentration'], color='darkorange',  label='the data')
    ax.legend()
    ax.tick_params(labelsize=7)
    ax.set_xlabel('Time (YY/MM)', fontsize=10)
    ax.set_ylabel('Measurement value (molarity)', fontsize=10)
    st.pyplot(fig)

    # st.markdown("Looks like the average publication date is around **{}**, with your oldest book being **{}** and your youngest being ****.")
    # st.markdown("Note that the publication date on Goodreads is the **last** publication date, so the data is altered for any book that has been republished by a publisher.")


st.write('')
st.markdown("""---""")
row4_space1, row4_1, row4_space2, row4_2, row4_space3 = st.beta_columns(
    (.1, 1, .1, 1, .1))

with row4_1, _lock:
    st.subheader("Venice Data")
    @st.cache(allow_output_mutation=True)
    def load_data():
        return veniceData()
    data_load_state = st.text('Loading data...')
    venice_df_tokyo = load_data()
    data_load_state.text('')
    st.dataframe(venice_df_tokyo)
    # year_to_filter = st.slider('Filter years', 2019, 2021, 2021, key='venice')  # min: 0h, max: 23h, default: 17h


with row4_2, _lock:
    st.subheader("Plot of Venice's Data")
    @st.cache(allow_output_mutation=True)
    def load_data():
        return  veniceData()
    data_load_state = st.text('Loading data...')
    venice_df_tokyo = load_data()
    data_load_state.text('')
    venice_df_tokyo.sort_values(by='Time', ascending=True, inplace=True)
    venice_df_tokyo['time'] = pd.to_datetime(venice_df_tokyo.Time)
    # venice_df_tokyo = venice_df_tokyo[chl_df_tokyo['time'].dt.year == year_to_filter]

    fig = Figure()
    ax = fig.subplots()
    # plt.figure(figsize=(15, 15))

    ax.plot(venice_df_tokyo['Time'], venice_df_tokyo['Chl_concentration'], color='darkorange',  label='the data')
    ax.legend()
    ax.tick_params(labelsize=7)
    ax.set_xlabel('Time (YY/MM)', fontsize=10)
    ax.set_ylabel('Measurement value (molarity)', fontsize=10)
    st.pyplot(fig)


st.write('')
st.markdown("""---""")
row5_space1, row5_1, row5_space2, row5_2, row5_space3 = st.beta_columns(
    (.1, 1, .1, 1, .1))

with row5_1, _lock:
    st.subheader("New York Data")
    @st.cache(allow_output_mutation=True)
    def load_data():
        return newYorkData()
    data_load_state = st.text('Loading data...')
    new_york_df_tokyo = load_data()
    data_load_state.text('')
    st.dataframe(new_york_df_tokyo)
    # year_to_filter = st.slider('Filter years', 2019, 2021, 2021, key='new-york')  # min: 0h, max: 23h, default: 17h


with row5_2, _lock:
    st.subheader("Plot of New-York's Data")
    @st.cache(allow_output_mutation=True)
    def load_data():
        return  newYorkData()
    data_load_state = st.text('Loading data...')
    new_york_df_tokyo = load_data()
    data_load_state.text('')
    new_york_df_tokyo.sort_values(by='Time', ascending=True, inplace=True)
    new_york_df_tokyo['time'] = pd.to_datetime(new_york_df_tokyo.Time)
    # new_york_df_tokyo = new_york_df_tokyo[chl_df_tokyo['time'].dt.year == year_to_filter]

    fig = Figure()
    ax = fig.subplots()
    # plt.figure(figsize=(15, 15))

    ax.plot(new_york_df_tokyo['Time'], new_york_df_tokyo['Chl_concentration'], color='darkorange',  label='the data')
    ax.legend()
    ax.tick_params(labelsize=7)
    ax.set_xlabel('Time (YY/MM)', fontsize=10)
    ax.set_ylabel('Measurement value (molarity)', fontsize=10)
    st.pyplot(fig)

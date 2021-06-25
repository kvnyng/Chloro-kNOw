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

from models.process_data import tokyoChlData
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
    @st.cache
    def load_data():
        return  tokyoChlData()
    data_load_state = st.text('Loading data...')
    df = load_data()
    data_load_state.text('')
    st.dataframe(df)

    df.sort_values(by='Time', ascending=True, inplace=True)
    df['time'] = pd.to_datetime(df.Time)
    
    plt.figure(figsize=(15, 15))
    plt.plot(df['time'], df['Measurement Value'], 'o-', color='darkorange')
    plt.tick_params(labelsize=15)
    plt.xlabel('Time (YY/MM)', fontsize=18)
    plt.ylabel('Measurement value (whatevermol)', fontsize=18)


    # hist_data = [df['Measurement Value'], df['Time']]
    # group_labels = ['Chl Concentration', 'Date']
    # fig = ff.create_distplot(hist_data, group_labels, bin_size=[10, 25])
    # st.plotly_chart(fig, use_container_width=True)
    # ax = fig.subplots()
    # if has_records:
    #     year_df = pd.DataFrame(
    #         df['read_at_year'].dropna().value_counts()).reset_index()
    #     year_df = year_df.sort_values(by='index')
    #     fig = Figure()
    #     ax = fig.subplots()
    #     sns.barplot(x=year_df['index'],
    #                 y=year_df['read_at_year'], color='goldenrod', ax=ax)
    #     ax.set_xlabel('Year')
    #     ax.set_ylabel('Books Read')
    #     st.pyplot(fig)
    # else:
    # st.markdown("Looks like the average publication date is around **{}**, with your oldest book being **{}** and your youngest being ****.")
    # st.markdown("Note that the publication date on Goodreads is the **last** publication date, so the data is altered for any book that has been republished by a publisher.")


with row3_2, _lock:
    st.subheader("Plot of Tokyo's Data")
    @st.cache
    def load_data():
        return  tokyoChlData()
    data_load_state = st.text('Loading data...')
    df = load_data()
    data_load_state.text('')
    # PUT WHAT YOU WANT (THE PLOT)
    # ax = fig.subplots()
    # sns.histplot(pd.to_numeric(df['book.publication_year'], errors='coerce').dropna(
    # ).astype(np.int64), kde_kws={'clip': (0.0, 2020)}, ax=ax, kde=True)
    # ax.set_xlabel('Book Publication Year')
    # ax.set_ylabel('Density')
    # st.pyplot(fig)
    #
    # avg_book_year = str(
    #     int(np.mean(pd.to_numeric(df['book.publication_year']))))
    # row = df[df['book.publication_year'] == str(
    #     pd.to_numeric(df['book.publication_year']).min())[0:4]]
    # oldest_book = row['book.title_without_series'].iloc[0]
    # row_young = df[df['book.publication_year'] == str(
    #     pd.to_numeric(df['book.publication_year']).max())[0:4]]
    # youngest_book = row_young['book.title_without_series'].iloc[0]

    # st.markdown("Looks like the average publication date is around **{}**, with your oldest book being **{}** and your youngest being ****.")
    # st.markdown("Note that the publication date on Goodreads is the **last** publication date, so the data is altered for any book that has been republished by a publisher.")

st.write('')
row4_space1, row4_1, row4_space2, row4_2, row4_space3 = st.beta_columns(
    (.1, 1, .1, 1, .1))

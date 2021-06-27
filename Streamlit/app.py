from matplotlib.backends.backend_agg import RendererAgg
import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
from matplotlib.figure import Figure
import altair as alt

import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.express as px
from models.process_data import tokyoData, veniceData, newYorkData


st.set_page_config(
        page_title="Nimbus Soulution",
        page_icon=":globe_with_meridians:",
        layout="wide")


matplotlib.use("agg")
_lock = RendererAgg.lock


sns.set_style('darkgrid')
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.beta_columns(
    (.1, 2, .2, 1, .1))



st.cache(persist=True)
def load_data():
    covid19 = pd.read_csv('data/covid.csv', encoding='ISO-8859-1',thousands='.', decimal=',', engine='python')
    covid19['date'] = pd.to_datetime(covid19['date'],format = '%Y-%m-%d')
    return covid19

data_load_state = st.text('Loading data, please wait...')
covid19 = load_data()
data_load_state.text('')


def main():
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


    # TOKYO COMPONENT
    with row3_1, _lock:
        st.header("Tokyo Data 🇯🇵 ")

        # Load Tokyo data.
        @st.cache(allow_output_mutation=True)
        def load_data():
            return tokyoData()
        data_load_state = st.text('Loading Tokyo data...')
        chl_df_tokyo = load_data()[0]
        tsm_df_tokyo = load_data()[1]
        data_load_state.text('')


        st.dataframe(load_data()[2])
        # year_to_filter = st.slider('Filter years', 2019, 2021, 2021, key='tokyo')  # min: 0h, max: 23h, default: 17h
        st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")



    with row3_2, _lock:
        st.header("Plot of Tokyo's Data")
        chl_df_tokyo.sort_values(by='Time', ascending=True, inplace=True)
        chl_df_tokyo['time'] = pd.to_datetime(chl_df_tokyo.Time)
        # chl_df_tokyo = chl_df_tokyo[chl_df_tokyo['time'].dt.year == year_to_filter]

        fig = Figure()
        ax = fig.subplots()
        plt.figure(figsize=(15, 15))

        ax.plot(chl_df_tokyo['Time'], chl_df_tokyo['Measurement Value'], color='darkorange',  label='Chl Concentration')
        ax.legend()
        ax.tick_params(labelsize=7)
        ax.set_xlabel('Time (YY/MM)', fontsize=10)
        ax.set_ylabel('Measurement value (molarity)', fontsize=10)
        st.pyplot(fig)

        # fig=px.bar(chl_df_tokyo,x='Time',y='Measurement Value')
        # fig.update_layout(title_x=0.5, xaxis_rangeslider_visible=True, legend=dict(x=-.5, y=-2))
        # fig.update_yaxes(title_text='Chlorophyll-A Concentration (Molarity)')
        # fig.update_xaxes(title_text='Date')
        # st.plotly_chart(fig)




    st.write('')
    row4_space1, row4_1, row4_space2, row4_2, row4_space3 = st.beta_columns(
        (.1, 1, .1, 1, .1))


    with row4_2, _lock:
        st.header("Cool dates for Japan")
        st.markdown('''The concentration of Chlorophyll-a is tested in lakes to determine how much algae is in the lake. Our solution shows the relationship between human activities and algae bloom, through out the COVID-19 pandemic human activities became decreasing and in result the concentration of Chl-a began decreasing to understand the dates below you must understand this first:
        \n Any decrease of the concentration of CHL was caused because of the high reported COVID-19 cases which meant less human activity in the past two months of the CHL decrease date.
        \n On the other hand, any increase of the concentration of CHL was caused because of the decrease of the reported COVID-19 cases which meant more human activity in the past two months of the CHL increase date.
        ''')
        expander_1 = st.beta_expander("The largest drop of concentration reported at 2020-08-22 in Japan.")
        expander_1.write('The largest drop of concentration was reported in 2020-08-22 with a decrease value of -87.3 in Tokyo, and if we look at the month before the date 2020-08-22 we can see the increase of COVID cases in Japan during the month of June and July of 2020:')
        button_1 = expander_1.button('Visualzie', key='3')
        button_1_end = expander_1.button('Stop Visualizing', key='3')


        expander_2 = st.beta_expander("The largest increase of concentration reported at 2019-11-09 in Japan.")
        expander_2.write('''The largest increase in the CHL concentration was reported in 2019-11-09 with an increase value of +265.03 in Tokyo, and if we take a look at the months before June we can realize that the increase happened before the Pandemic. ''')

    with row4_1, _lock:
        country = 'Japan'
        st.header("Japan Covid Cases")
        if button_1:
            japan_covid_fig=px.bar(covid19[covid19["location"]==country],x='date',y='new_cases', color='tokyo_increase_color')
            japan_covid_fig.update_layout(title_x=0.5, xaxis_rangeslider_visible=True)
            japan_covid_fig.update_yaxes(title_text='New Cases')
            japan_covid_fig.update_xaxes(title_text='Date')
            st.plotly_chart(japan_covid_fig)
        elif button_1_end:
            japan_covid_fig=px.bar(covid19[covid19["location"]==country],x='date',y='new_cases')
            japan_covid_fig.update_layout(title_x=0.5, xaxis_rangeslider_visible=True)
            japan_covid_fig.update_yaxes(title_text='New Cases')
            japan_covid_fig.update_xaxes(title_text='Date')
            st.plotly_chart(japan_covid_fig)
        else:
            japan_covid_fig=px.bar(covid19[covid19["location"]==country],x='date',y='new_cases')
            japan_covid_fig.update_layout(title_x=0.5, xaxis_rangeslider_visible=True)
            japan_covid_fig.update_yaxes(title_text='New Cases')
            japan_covid_fig.update_xaxes(title_text='Date')
            st.plotly_chart(japan_covid_fig)

    #ITALY
    st.write('')
    st.markdown("""---""")
    row5_space1, row5_1, row5_space2, row5_2, row5_space3 = st.beta_columns(
        (.1, 1, .1, 1, .1))

    with row5_1, _lock:
        st.header("Venice Data 🇮🇹")
        @st.cache(allow_output_mutation=True)
        def load_data():
            return veniceData()
        data_load_state = st.text('Loading Venice data...')
        chl_df_venice = load_data()[0]
        tsm_df_venice = load_data()[1]
        data_load_state.text('')
        st.dataframe(load_data()[2])
        # year_to_filter = st.slider('Filter years', 2019, 2021, 2021, key='venice')  # min: 0h, max: 23h, default: 17h
        st.markdown("Note that the publication date on Goodreads is the **last** publication date, so Chl Concentration is altered for any book that has been republished by a publisher.")


    with row5_2, _lock:
        st.header("Plot of Venice's Data ")
        chl_df_venice.sort_values(by='Time', ascending=True, inplace=True)
        chl_df_venice['time'] = pd.to_datetime(chl_df_venice.Time)
        # chl_df_venice = chl_df_venice[chl_df_tokyo['time'].dt.year == year_to_filter]
        fig = Figure()
        ax = fig.subplots()
        ax.plot(chl_df_venice['Time'], chl_df_venice['Measurement Value'], color='darkorange',  label='Chl Concentration')
        ax.legend()
        ax.tick_params(labelsize=7)
        ax.set_xlabel('Time (YY/MM)', fontsize=10)
        ax.set_ylabel('Measurement value (molarity)', fontsize=10)
        st.pyplot(fig)
        # fig=px.bar(chl_df_venice,x='Time',y='Measurement Value')
        # fig.update_layout(title_x=0.5, xaxis_rangeslider_visible=True, legend=dict(x=-.5, y=-2))
        # fig.update_yaxes(title_text='Chlorophyll-A Concentration (Molarity)')
        # fig.update_xaxes(title_text='Date')
        # st.plotly_chart(fig)


    st.write('')
    row6_space1, row6_1, row6_space2, row6_2, row6_space3 = st.beta_columns(
        (.1, 1, .1, 1, .1))


    with row6_2, _lock:
        st.header("Cool dates for Italy")
        st.markdown('''The concentration of Chlorophyll-a is tested in lakes to determine how much algae is in the lake. Our solution shows the relationship between human activities and algae bloom, through out the COVID-19 pandemic human activities became decreasing and in result the concentration of Chl-a began decreasing to understand the dates below you must understand this first:
        \n Any decrease of the concentration of CHL was caused because of the high reported COVID-19 cases which meant less human activity in the past two months of the CHL decrease date.
        \n On the other hand, any increase of the concentration of CHL was caused because of the decrease of the reported COVID-19 cases which meant more human activity in the past two months of the CHL increase date.
        ''')
        expander_1 = st.beta_expander("The largest drop of concentration reported at 2020-08-22.")
        expander_1.write('The largest drop of Chl-a concentration was reported in 2021-03-06 with a decrease value of -79.630008 in Venice, and if we look at the months before the date 2021-03-06  we can see the increase of COVID cases in Italy during the months of January and February of 2021:')
        button_2 = expander_1.button('Visualzie', key='12')
        button_2_end = expander_1.button('Stop Visualzing', key='11')



        expander_2 = st.beta_expander("The largest increase of concentration reported at 2019-11-09.")
        expander_2.write('''The largest increase in the CHL concentration was reported in 2019-06-13 with an increase value of +400.38177 in Venice, and if we take a look at the months before June we can realize that the increase happened before the Pandemic. ''')


    with row6_1, _lock:
        if button_2:
            country = 'Italy'
            st.header("Italy Covid Cases")
            italy_covid_fig=px.bar(covid19[covid19["location"]==country],x='date',y='new_cases', color='italy_increase_color')
            italy_covid_fig.update_layout(title_x=0.5, xaxis_rangeslider_visible=True)
            italy_covid_fig.update_yaxes(title_text='New Cases')
            italy_covid_fig.update_xaxes(title_text='Date')
            st.plotly_chart(italy_covid_fig)
        elif button_2_end:
            country = 'Italy'
            st.header("Italy Covid Cases")
            italy_covid_fig=px.bar(covid19[covid19["location"]==country],x='date',y='new_cases')
            italy_covid_fig.update_layout(title_x=0.5, xaxis_rangeslider_visible=True)
            italy_covid_fig.update_yaxes(title_text='New Cases')
            italy_covid_fig.update_xaxes(title_text='Date')
            st.plotly_chart(italy_covid_fig)
        else:
            country = 'Italy'
            st.header("Italy Covid Cases")
            italy_covid_fig=px.bar(covid19[covid19["location"]==country],x='date',y='new_cases')
            italy_covid_fig.update_layout(title_x=0.5, xaxis_rangeslider_visible=True)
            italy_covid_fig.update_yaxes(title_text='New Cases')
            italy_covid_fig.update_xaxes(title_text='Date')
            st.plotly_chart(italy_covid_fig)

    #UNITED STATES
    st.write('')
    st.markdown("""---""")
    row7_space1, row7_1, row7_space2, row7_2, row7_space3 = st.beta_columns(
        (.1, 1, .1, 1, .1))

    with row7_1, _lock:
        st.header("New York Data 🇺🇸 ")
        @st.cache(allow_output_mutation=True)
        def load_data():
            return newYorkData()
        data_load_state = st.text('Loading New York data...')
        chl_df_newyork = load_data()[0]
        tsm_df_newyork = load_data()[1]
        data_load_state.text('')
        st.dataframe(load_data()[2])
        # year_to_filter = st.slider('Filter years', 2019, 2021, 2021, key='new-york')  # min: 0h, max: 23h, default: 17h
        st.markdown("Note that the publication date on Goodreads is the **last** publication date, so Chl Concentration is altered for any book that has been republished by a publisher.")



    with row7_2, _lock:
        st.header("Plot of New-York's Data")
        chl_df_newyork.sort_values(by='Time', ascending=True, inplace=True)
        chl_df_newyork['time'] = pd.to_datetime(chl_df_newyork.Time)
        # chl_df_newyork = chl_df_newyork[chl_df_tokyo['time'].dt.year == year_to_filter]

        fig = Figure()
        ax = fig.subplots()
        # plt.figure(figsize=(15, 15))
        ax.plot(chl_df_newyork['Time'], chl_df_newyork['Measurement Value'], color='darkorange',  label='Chl Concentration')
        ax.legend()
        ax.tick_params(labelsize=7)
        ax.set_xlabel('Time (YY/MM)', fontsize=10)
        ax.set_ylabel('Measurement value (molarity)', fontsize=10)
        st.pyplot(fig)
        # fig=px.bar(chl_df_newyork,x='Time',y='Measurement Value')
        # fig.update_layout(title_x=0.5, xaxis_rangeslider_visible=True, legend=dict(x=-.5, y=-2))
        # fig.update_yaxes(title_text='Chlorophyll-A Concentration (Molarity)')
        # fig.update_xaxes(title_text='Date')
        # st.plotly_chart(fig)




    st.write('')
    row8_space1, row8_1, row8_space2, row8_2, row8_space3 = st.beta_columns(
        (.1, 1, .1, 1, .1))

    with row8_1, _lock:
        country = 'United States'
        st.header("United States Covid Cases")
        fig=px.bar(covid19[covid19["location"]==country],x='date',y='new_cases')
        fig.update_layout(title_x=0.5, xaxis_rangeslider_visible=True, legend=dict(x=-.5, y=-2))
        fig.update_yaxes(title_text='New Cases')
        fig.update_xaxes(title_text='Date')
        st.plotly_chart(fig)

    with row8_2, _lock:
        st.header("Cool dates for New York")
        st.markdown('Coming soon...')

if __name__ == '__main__':
    main()

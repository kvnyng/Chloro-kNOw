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
from models.process_data import tokyoData, veniceData, newYorkData, movingAverage
import streamlit.components.v1 as components

st.set_page_config(
        page_title="Nimbus Solution ",
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
        'Solution by the [Nimbus Team](https://github.com/bykevinyang/Nimbus)')

    row1_spacer1, row1_1, row1_spacer2 = st.beta_columns((.1, 3.2, .1))

    with row1_1:
        st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

    st.markdown("""---""")
    st.write('')
    row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.beta_columns(
        (.1, 1, .1, 1, .1))
    # country = st.multiselect('Select a country', ['Japan', 'Italy', 'United States'])
    with row3_1, _lock:
        st.header("Tokyo Data 🇯🇵 ")

        # Load Tokyo data.
        @st.cache(allow_output_mutation=True)
        def load_data():
            return tokyoData()


        data_load_state = st.text('Loading Tokyo data...')
        chl_df_tokyo = load_data()[0]
        air_df_tokyo = load_data()[1]
        activity_df_japan = load_data()[2]
        data_load_state.text('')


        st.dataframe(load_data()[-1])
        st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")


    with row3_2, _lock:
        st.header("Chlorophyll-a concentration in Japan")
        chl_df_tokyo.sort_values(by='Time', ascending=True, inplace=True)

        chl_df_tokyo['time'] = pd.to_datetime(chl_df_tokyo.Time)
        fig = Figure()
        ax = fig.subplots()
        plt.figure(figsize=(15, 15))
        smoothed = movingAverage()
        ax.plot(chl_df_tokyo['Time'], chl_df_tokyo['Measurement Value'], color='darkorange',  label='Chl Concentration')
        # ax.plot(smoothed['Time'], smoothed['Smoothed'], color='darkorange',  label='Chl Concentration')
        # ax.plot(covid19[covid19["location"]=='Japan']['date'], covid19[covid19["location"]=='Japan']['new_cases']/20/2, color='green',  label='Covid cases')
        ax.legend()
        ax.tick_params(labelsize=7)
        ax.set_xlabel('Time (YY/MM)', fontsize=10)
        ax.set_ylabel('Measurement value (molarity)', fontsize=10)
        st.pyplot(fig)

    st.write('')
    row4_space1, row4_1, row4_space2, row4_2, row4_space3 = st.beta_columns(
        (.1, 1, .1, 1, .1))

    with row4_2, _lock:
        st.header("Interesting dates for Japan")
        st.markdown('''The concentration of Chlorophyll-a is tested in lakes to determine how much algae is in the lake. Our solution shows the relationship between human activities and algae bloom, through out the COVID-19 pandemic human activities became decreasing and in result the concentration of Chl-a began decreasing to understand the dates below you must understand this first:
        \n Any decrease of the concentration of CHL was caused because of the high reported COVID-19 cases which meant less human activity in the past two months of the CHL decrease date.
        \n On the other hand, any increase of the concentration of CHL was caused because of the decrease of the reported COVID-19 cases which meant more human activity in the past two months of the CHL increase date.
        ''')
        expander_1 = st.beta_expander("The largest drop of concentration reported at 2020-08-22 in Japan.")
        expander_1.write('The largest drop of concentration was reported in 2020-08-22 with a decrease value of -87.3 in Tokyo, and if we look at the month before the date 2020-08-22 we can see the increase of COVID cases in Japan during the month of June and July of 2020:')
        button_1 = expander_1.button('Visualize', key='3')
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

    st.write('')
    row5_space1, row5_1, row5_space2, row5_2, row5_space3 = st.beta_columns(
        (.1, 1, .1, 1, .1))

    with row5_1, _lock:
        st.header("Chlorophyll-a concentration map in Japan")
        components.html('<iframe class="item" src="https://eodashboard.org/iframe?poi=JP01-N3a2"  width="600px" height="500px" frameBorder="0" scroll="no" style="overflow:hidden"></iframe>', height=500, width=1000)
        st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")

    with row5_2, _lock:
        st.header("Recovery Proxy map in Japan")
        components.html('<iframe class="item" src="https://eodashboard.org/iframe?poi=JP01-N8" width="600px" height="500px" frameBorder="0" scroll="no" style="overflow:hidden"></iframe>', height=500,width=1000)
        st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")


    st.write('')
    row6_space1, row6_1, row6_space2, row6_2, row6_space3 = st.beta_columns(
        (.1, 1, .1, 1, .1))

    with row6_1, _lock:
        st.header("Air quality measurement in Japan")
        japan_air_fig=px.bar(air_df_tokyo,x='time',y='measurement')
        japan_air_fig.update_layout(title_x=0.5, xaxis_rangeslider_visible=True)
        japan_air_fig.update_yaxes(title_text='Air Quality Index')
        japan_air_fig.update_xaxes(title_text='Date')
        st.plotly_chart(japan_air_fig)
        st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")

    with row6_2, _lock:
        st.header("Cars/Containers Acttivity in Japan")
        japan_activity_fig = px.bar(activity_df_japan,x='time',y='measurement', color='colorCode')
        japan_activity_fig.update_layout(title_x=0.5, xaxis_rangeslider_visible=True)
        japan_activity_fig.update_yaxes(title_text='New Cases')
        japan_activity_fig.update_xaxes(title_text='Date')
        st.plotly_chart(japan_activity_fig)
        st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")



if __name__ == '__main__':
    main()

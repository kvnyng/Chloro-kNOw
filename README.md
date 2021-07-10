[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/janinirami/chloro-know/main/app.py)

# Chloro-Know
Chloro-kNOw is an online dashboard that relates factors that affect chlorophyll (Chl) concentrations in order to draw relationships between COVID-19 and its effects on Chl concentrations. With chloro-kNOw, we aim to raise awareness about daily actions that can lead to increases in algal blooms and mitigate them in order to keep our water clean for the generations to come. Be in the know to tell chloro no! 

# Project Demo
* Video demo: https://youtu.be/DpcNKZ0--_0

* Live site: https://share.streamlit.io/janinirami/chloro-know/main/app.py

# How We Addressed This Challenge

In the past few years, eutrophication and algal blooms have been on the rise. This has had detrimental effects on the environment, and civilization. Most recently officials in the state of Wisconsin had to close beaches due to a toxic cyanobacteria bloom that left dead fish floating on the beaches. However, algal blooms are not just showing up along Wisconsin lakes, but also the Great Lakes, the coast of Florida, and even in the Baltic Sea. 
![Ocean](https://eohack-assets.eodashboardhackathon.org/media/images/59076d09-f8da-4d0e-8854-025a394b9b0e.max-1000x1000.jpg)
	Toxic to both humans and pets, algae, such as cyanobacteria, can consume all the oxygen in the water and produce harmful toxins that can kill off dogs. This poses a problem environmentally due to its impact on local fish populations and its potential health consequences on humans. Just a few months prior, a toxic algal bloom appeared in Utah Lake, leaving the surrounding area waterless due to the cyanobacteria. 

This increase in algal blooms is attributed to human related factors, such as excess fertilizer usage that is running into local riverways.

Nevertheless, despite this general increase in eutrophication, looking at recent chlorophyll-a anomaly data from this past year we have found a weak link between COVID-19 and algal blooms, we have realized that COVID-19 is not playing much of a role one way or another in the bloom this past year. Lots of it is fueled by farm run off and the farmers who have not stopped working during the pandemic due to the demand for food. Although COVID-19 did have some effects as the biggest increase of Chlorophyll-a concentration in Japan was actually before the COVID-19 cases; which makes sense because they were no restrictions on human activities at that time, but this is not true for all countries, as there isn't much changing at wastewater plants; people are still putting fertilizer on the lawns. So it's not expected COVID-19 will have a strong effect either way.

Using Chloro-kNOw you can take a personal look at all these data (Provided by NASA, JAXA, ESA and other sources) and even challenge yourself to find some relationships between wind data, human activity data and COVID-19 data with Chlorophyll concentrations, Of course one of the other main reasons we created Chloro-kNOw is to raise awareness about the harm some us humans do in our daily life towards water through algal blooms and suggest ways to prevent this harm to keep our water clean for the future generations to come.

# How We Developed This Project

We developed this project by first researching algal blooms, its causes, and ways to mitigate it, and then searching for datasets that we could implement into the dashboard. 

We were inspired to do this challenge because one of our teammates was personally impacted by algal blooms, and as we researched more about algal blooms, realized that its impact went much farther than a local tap water problem.

On the technical side, we wrote the project using almost entirely python. We sadly lacked a front end developer, so we used a python library called streamlit, that converts python code into components like vue.js and react.js. As for the backend, we wrote scripts that cleaned and analysed incoming data from the EO dashboard (as well as other datasets). To plot such data, we either used the EO dashboard API’s, matplotlib or streamlit. We also wrote a few programs to get statistical correlations between different factors using python libraries such as numpy and pandas. 

The biggest problem we faced was having a committed team. Originally we had 6 members on Chloro-kNOw, but due to external time commitments, 3 of our teammates sadly had to leave the competition. With a smaller tea and less time, we were constantly under pressure in trying to finish before the submission deadline. This led us to having to use streamlit since our frontend person left. In addition, we also struggled in finding datasets that were about factors that we deemed important, such as fertilizer usage or river discharge. With a little more time and a larger team, we could have created our own dataset on fertilizer usage by looking at farm land and its vegetation index, thus making up for the lack of fertilizer usage data that plays such a vital role in eutrophication (this is similar to a process used by OneSoil). 

# How I Used Space Agency Data in This Project

The majority of our data comes directly from the EO dashboard. We took data such as air quality, water quality, wind, nightlight, and human activity and related that to external data that we found such as COVID-19 cases data. 

The data we had access to heavily influenced our project. Since the dashboard is entirely data based, what we have access to is what we can do. Despite our limitation in datasets about factors we were curious to see (such as fertilizer usage), we made due with the available datasets we had. This ultimately shaped the look of the dashboard. 

On the other hand, with the data we had access to we created heat maps and graphs, and ran correlation analysis between each factor. 

# Earth Observing Dashboard Integration

Alongside COVID-19 cases and chlorophyll concentration, our project processes, cleans, analyzes and displays in-situ data using clever python algorithms. Using a python library called ‘Streamlit’, we can convert our app to an API with a user-friendly front end. To do this, a bi-directional component provided by Streamlit will be used. This the bi-directional component will have two parts:

* The first part will be the front-end which is built in any front-end web tech such as Vue.js where it is used in js the EODashboard
* The second part will be a python api which Streamlit apps use to instantiate and talk to that frontend (EODashboard in this case).
* Note: A bi-directional component solution is provided in Streamlit’s documentation.

Our solution can be integrated as a separate page from the indicators, allowing non-scientific people to understand the data and the correlations between algal blooms and other in-situ data, such as COVID-19 cases, wind quality and recovery proxy of human activities. Under each plot, we have also included a detailed description that explains what is being shown and any notable trends that appear. In this way we are able to show meanings and relationships to everyone, regardless of their expertise. 

# Data & Resources
 * Chlorophyll-a concentration time-series: https://eodashboard.org/?indicator=N3b
 *  Chlorophyll-a concentration map for Japan: https://eodashboard.org/?indicator=N3a2&poi=JP01-N3a2
 * Tokyo air quality: https://eodashboard.org/?indicator=N1&poi=JP01-N1
 *  Recovery proxy map: https://eodashboard.org/?indicator=N8&poi=JP01-N8
 *  Cars and containers activity: https://eodashboard.org/?indicator=E9&poi=JP01-N8
 *  COVID-19 data: https://github.com/owid/covid-19-data
 
 
 # Authors
 * [Rami Janini](https://github.com/JaniniRami) (Head Developer)
 * [Kevin Yang](https://github.com/bykevinyang) (Developer + Writer)
 * [George Adamopoulos](https://github.com/george-adams1) (Developer)

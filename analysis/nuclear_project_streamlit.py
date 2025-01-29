import json 
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import streamlit as st
import plotly.express as px
import folium 
from folium.plugins import MarkerCluster
from PIL import Image
import base64
from io import BytesIO


#Read the CSV Files
df_global_power_plants=pd.read_csv('global_power_plant_database_last.csv')
df_energy_consumption=pd.read_csv('Primary-energy-consumption-from-fossilfuels-nuclear-renewables.csv')
df_elec_production=pd.read_csv('share-elec-produc-by-source.csv')
df_emissions=pd.read_csv('annual-co2-emissions-per-country-2.csv')
df_mineral_ores=pd.read_csv('Mineral_ores_round_the_world.csv')
df_earthquakes=pd.read_csv("Earthquakes.csv")

#Drop the columns that we are not use in our analysis
df_global_power_plants.drop(columns=['estimated_generation_note_2013','estimated_generation_note_2014','estimated_generation_note_2015','estimated_generation_note_2016','estimated_generation_note_2017'],inplace=True)
df_global_power_plants.drop(columns=['source','url','geolocation_source'],inplace=True)
df_global_power_plants.drop(columns=['other_fuel2','other_fuel3'],inplace=True)
df_global_power_plants.drop(columns=['wepp_id'],inplace=True)
df_global_power_plants.drop(columns=['generation_data_source'],inplace=True)


#Create a dictionairy whose key-values is the categorization of our countries in level of continents 
regions = {
    "Asia": [
        "Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei Darussalam", 
        "Cambodia", "China", "Cyprus", "Georgia", "India", "Indonesia", "Iran", "Iraq", "Israel", 
        "Japan", "Jordan", "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", 
        "Maldives", "Mongolia", "Myanmar", "Nepal", "North Korea", "Oman", "Pakistan", "Palestine", 
        "Philippines", "Qatar", "Saudi Arabia", "Singapore", "South Korea", "Sri Lanka", "Syria", 
        "Tajikistan", "Thailand", "Timor-Leste", "Turkey", "Turkmenistan", "United Arab Emirates", 
        "Uzbekistan", "Vietnam", "Yemen","Syrian Arab Republic","Taiwan","Western Sahara"
    ],
    "Europe": [
        "Albania", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia", 
        "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", 
        "Iceland", "Ireland", "Italy", "Kosovo", "Latvia", "Lithuania", "Luxembourg", "Macedonia", 
        "Moldova", "Montenegro", "Netherlands", "Norway", "Poland", "Portugal", "Romania", "Russia", 
        "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine", "United Kingdom"
    ],
    "Africa": [
        "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cameroon", "Cape Verde", 
        "Central African Republic", "Chad", "Comoros", "Congo", "Djibouti", "Egypt", "Equatorial Guinea", 
        "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", 
        "Ivory Coast", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", 
        "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", 
        "Sao Tome and Principe", "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", 
        "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe","Cote DIvoire","Democratic Republic of the Congo","Swaziland"
    ],
    "North America": [
        "Canada", "United States of America", "Mexico", "Jamaica", "Honduras", "Guatemala", "Cuba", 
        "Panama", "Costa Rica", "El Salvador", "Bahamas", "Barbados", "Dominican Republic", "Haiti", 
        "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Trinidad and Tobago","Nicaragua"
    ],
"South America": [
        "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Guyana", "Paraguay", 
        "Peru", "Suriname", "Uruguay", "Venezuela","French Guiana"
    ],
"Oceania": [
        "Australia", "Fiji", "Kiribati", "Marshall Islands", "Micronesia", "Nauru", "New Zealand", 
        "Palau", "Papua New Guinea", "Samoa", "Solomon Islands", "Tonga", "Tuvalu", "Vanuatu"
    ]
,
"Antarctica":["Antarctica"]
}


#Make a function that filters every country of the "country_long" column,gives the continent that is contained and put it in order in a new list.
continents_global_powerplants=[]
for country in df_global_power_plants['country_long']:
    for key,value in regions.items():
        if country in value:
            continents_global_powerplants.append(key)

#Insert a new column in DataFrame that contains the continent,based on the list that we made.
df_global_power_plants['continent']=continents_global_powerplants

#Make a dictionairy that key-values is a general categorization of "primary_fuel" elements.
energy_sources = {
    "Fossil Fuels": ["Gas", "Oil", "Coal", "Petcoke"],
    "Nuclear": ["Nuclear"],
    "Renewables": 
       [ "Hydro", "Solar", "Wind", "Waste", "Biomass", 
        "Wave and Tidal", "Geothermal"],
"Other": ["Other", "Storage", "Cogeneration" ]
} 

#Filters the "primary_fuel" column to see in which general fuel category (key) of energy_sources dictionairy contained.
energy_type=[]
for source in df_global_power_plants['primary_fuel']:
    for key,value in energy_sources.items():
        if source in value:
            energy_type.append(key)


#Insert a new column in DataFrame that contains the general fuel category, based on the list that we made.
df_global_power_plants['energy_type']=energy_type


#Round the elements of specified float type columns.
df_energy_consumption['Fossil fuels (% sub energy)']=df_energy_consumption['Fossil fuels (% sub energy)'].round(2)
df_energy_consumption['Renewables (% sub energy)']=df_energy_consumption['Renewables (% sub energy)'].round(2)
df_energy_consumption['Nuclear (% sub energy)']=df_energy_consumption['Nuclear (% sub energy)'].round(2)

#We keep only from the "Entity" column that has specified entries that we interested for our analysis.
df_energy_consumption=df_energy_consumption[(df_energy_consumption['Entity']!='Europe') & (df_energy_consumption['Entity']!='North America') & (df_energy_consumption['Entity']!='Africa')]

#Create a dictionairy whose key-values is the categorization of our countries in level of continents
regions= {
    "Asia": [
        "Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei Darussalam", 
        "Cambodia", "China", "Cyprus", "Georgia", "India", "Indonesia", "Iran", "Iraq", "Israel", 
        "Japan", "Jordan", "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", 
        "Maldives", "Mongolia", "Myanmar", "Nepal", "North Korea", "Oman", "Pakistan", "Palestine", 
        "Philippines", "Qatar", "Saudi Arabia", "Singapore", "South Korea", "Sri Lanka", "Syria", 
        "Tajikistan", "Thailand", "Timor-Leste", "Turkey", "Turkmenistan", "United Arab Emirates", 
        "Uzbekistan", "Vietnam", "Yemen","Syrian Arab Republic","Taiwan","Western Sahara","Hong Kong"
    ],
    "Europe": [
        "Albania", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia", 
        "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", 
        "Iceland", "Ireland", "Italy", "Kosovo", "Latvia", "Lithuania", "Luxembourg", "Macedonia", 
        "Moldova", "Montenegro", "Netherlands", "Norway", "Poland", "Portugal", "Romania", "Russia", 
        "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine", "United Kingdom","Czechia","North Macedonia"
    ],
    "Africa": [
        "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cameroon", "Cape Verde", 
        "Central African Republic", "Chad", "Comoros", "Congo", "Djibouti", "Egypt", "Equatorial Guinea", 
        "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", 
        "Ivory Coast", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", 
        "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", 
        "Sao Tome and Principe", "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", 
        "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe","Cote DIvoire","Democratic Republic of the Congo","Swaziland"
    ],
    "North America": [
        "Canada", "United States of America", "Mexico", "Jamaica", "Honduras", "Guatemala", "Cuba", 
        "Panama", "Costa Rica", "El Salvador", "Bahamas", "Barbados", "Dominican Republic", "Haiti", 
        "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Trinidad and Tobago","Nicaragua","United States"
    ],
"South America": [
        "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Guyana", "Paraguay", 
        "Peru", "Suriname", "Uruguay", "Venezuela","French Guiana"
    ],
"Oceania": [
        "Australia", "Fiji", "Kiribati", "Marshall Islands", "Micronesia", "Nauru", "New Zealand", 
        "Palau", "Papua New Guinea", "Samoa", "Solomon Islands", "Tonga", "Tuvalu", "Vanuatu"
    ]
,
"Antarctica":["Antarctica"]
    ,
    "World":["World"]
}


#We filter the elements of "Entity" column,gives the continent that is contained and put it in order in a new list.
continents_energy_consumption=[]
for country in df_energy_consumption['Entity']:
    for key,value in regions.items():
        if country in value:
            continents_energy_consumption.append(key)


#Insert a new column in DataFrame that contains the continent,based on the list that we made.
df_energy_consumption['Continent']=continents_energy_consumption

#Round the elements of specified float type columns.
df_elec_production['Coal (% electricity)']=df_elec_production['Coal (% electricity)'].round(2)
df_elec_production['Gas (% electricity)']=df_elec_production['Gas (% electricity)'].round(2)
df_elec_production['Hydro (% electricity)']=df_elec_production['Hydro (% electricity)'].round(2)
df_elec_production['Solar (% electricity)']=df_elec_production['Solar (% electricity)'].round(2)
df_elec_production['Wind (% electricity)']=df_elec_production['Wind (% electricity)'].round(2)
df_elec_production['Wind (% electricity)']=df_elec_production['Wind (% electricity)'].round(2)
df_elec_production['Oil (% electricity)']=df_elec_production['Oil (% electricity)'].round(2)
df_elec_production['Nuclear (% electricity)']=df_elec_production['Nuclear (% electricity)'].round(2)
df_elec_production['Other renewables (% electricity)']=df_elec_production['Other renewables (% electricity)'].round(2)

#We keep only from the "Entity" column that has specified entries that we interested for our analysis.
df_elec_production=df_elec_production[(df_elec_production['Entity']=='Europe') | (df_elec_production['Entity']=='North America') | (df_elec_production['Entity']=='Africa') | (df_elec_production['Entity']=='Australia') | (df_elec_production['Entity']=='South & Central America') | (df_elec_production['Entity']=='World')|(df_elec_production['Entity']=='Asia Pacific')]


#We replace values of "Entity" column to be the same as Energy Consumption's Entity column.
df_elec_production = df_elec_production.replace('Entity',{
    'Australia': 'Oceania',
    'South & Central America': 'South America',
    'Asia Pacific':'Asia'
})

#We summarized the values some columns to make two new columns .
df_elec_production['Fossil Fuels(% electricity)'] = df_elec_production['Coal (% electricity)'] + df_elec_production['Gas (% electricity)'] + df_elec_production['Oil (% electricity)']
df_elec_production['Renewables(% electricity)'] = df_elec_production['Hydro (% electricity)'] + df_elec_production['Solar (% electricity)'] + df_elec_production['Wind (% electricity)'] + df_elec_production['Other renewables (% electricity)']

#Define the "commod1" elements concerning uranium minerals.
df_minerals_uranium = df_mineral_ores[df_mineral_ores['commod1'].astype(str).str.contains(r'\bUranium\b', case=False, na=False)]

#Create a list of the column names that we want to drop.
columns_to_drop = [
    'commod2', 'commod3', 'oper_type', 'dep_type', 'prod_size', 
    'dev_stat', 'ore', 'gangue', 'work_type', 'names', 
    'ore_ctrl', 'hrock_type', 'arock_type']

#We keep only the rows concerning uranium minerals.
df_minerals_uranium_only = df_minerals_uranium.drop(columns=columns_to_drop, errors='ignore')

#Change the type of "Annual CO₂ emissions" column elements to millions.
df_emissions['Annual CO₂ emissions']=(df_emissions['Annual CO₂ emissions'].astype(float)/1000000).round(2)

df_global_power_plants = df_global_power_plants.rename(columns={'continent': 'Entity'})
df_energy_consumption = df_energy_consumption.rename(columns={
    'Entity': 'Country',
    'Continent': 'Entity'
})

st.set_page_config(layout="wide")
st.sidebar.title("Page ")
page = st.sidebar.radio("Select a page", [ "Fuel Trends in Energy Consumption and Energy Production", "Power Plants Energy Capacity","Power Plants & Fuel Usage","Investment Opportunities"])




if page=="Fuel Trends in Energy Consumption and Energy Production":

    st.title("Fuel Trends in Energy Consumption and Energy Production")
    image_path = r'background_12.06.33_PM.jpg'
    image = Image.open(image_path)


    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()


    st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url('data:image/jpeg;base64,{img_str}');
                background-size: cover;
                background-position: center;
            }}
            </style>
            """, unsafe_allow_html=True)

    

    Continent = st.sidebar.multiselect("Continent:", df_global_power_plants["Entity"].unique())

    #Function to filter all graphs by continent (Entity column) else return full graph
    def filter_by_continent(df, continents):
        if continents:
            return df[df["Entity"].isin(continents)]
        else:
            return df

    filtered_power_plants = filter_by_continent(df_global_power_plants, Continent)
    filtered_energy_consumption = filter_by_continent(df_energy_consumption, Continent)
    filtered_elec_production = filter_by_continent(df_elec_production, Continent)
    filtered_emissions = filter_by_continent(df_emissions, Continent)


    
    lst_of_years=filtered_energy_consumption.reset_index()['Year'].unique()
    selected_year_range = st.slider(
        "Select a range of years", 
        min_value=filtered_energy_consumption .reset_index()['Year'].min(), 
        max_value=filtered_energy_consumption .reset_index()['Year'].max(), 
        value=(1965, 2019), 
        step=1
    )
    filtered_energy_consumption = filtered_energy_consumption[(filtered_energy_consumption ["Year"] >= selected_year_range[0]) & (filtered_energy_consumption ["Year"] <= selected_year_range[1])]
    filtered_elec_production=filtered_elec_production[(filtered_elec_production["Year"]>= selected_year_range[0]) & (filtered_elec_production["Year"] <= selected_year_range[1])]


    continent_colors_palette = {
    "Asia": "yellow",
    "Europe": "blue",
    "Africa": "green",
    "North America": "red",
    "South America": "purple",
    "Oceania": "brown",
    }

    col1,col2=st.columns(2)
    with col1:
        st.subheader('Continents energy production by type of fuel')
        fuel_types = ['Nuclear (% electricity)','Renewables(% electricity)','Fossil Fuels(% electricity)']

        for fuel in fuel_types:
            fig1=px.line(filtered_elec_production,x='Year',y=fuel,color='Entity',labels={'Entity':'Continent'},hover_name=fuel,title=f'Energy Production by {fuel} : Yearly Trends per Continent',color_discrete_map=continent_colors_palette)
            fig1.update_layout(height=500,showlegend=True)
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader('Continents energy consumption by type of fuel')
        lst=['Nuclear (% sub energy)','Renewables (% sub energy)','Fossil fuels (% sub energy)']
        for k in lst:
            Nuclear_Energy_Consumption=filtered_energy_consumption.groupby(['Year','Entity'])[k].sum().unstack()
            fig2=px.line(Nuclear_Energy_Consumption.reset_index(),x='Year',y=Nuclear_Energy_Consumption.columns,labels={'value':f'{k} Consumption','variable':'Continent'},title=f'Energy Consumption by {k} : Yearly Trends per Continent',color_discrete_map=continent_colors_palette)
            fig2.update_layout(height=500,showlegend=True)
            st.plotly_chart(fig2, use_container_width=True)

elif page=="Power Plants Energy Capacity":
    st.title("Power Plants Energy Capacity")
    image_path = r'background_12.06.33_PM.jpg'
    image = Image.open(image_path)


    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()


    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('data:image/jpeg;base64,{img_str}');
            background-size: cover;
            background-position: center;
        }}
        </style>
        """, unsafe_allow_html=True)

    st.header('Energy Capacity Distribution around the World')

    Continent = st.sidebar.multiselect("Continent:", df_global_power_plants["Entity"].unique())

     
     #Function to filter all graphs by continent (Entity column) else return full graph
    def filter_by_continent(df, continents):
        if continents:
            return df[df["Entity"].isin(continents)]
        else:
            return df

    filtered_power_plants = filter_by_continent(df_global_power_plants, Continent)


    df_capacity_per_country = (
        filtered_power_plants
        .groupby('country_long')
        .agg({'capacity_mw': 'sum'})
        .sort_values(by='capacity_mw', ascending=False)
        .reset_index()
        .head(20)
    )
    
    df_total=filtered_power_plants.groupby(['country_long','Entity'])['capacity_mw'].sum().sort_values(ascending=False).head(20).reset_index()

    ###Added card total energy capaity
    total_energy_capacity = filtered_power_plants['capacity_mw'].sum()

    st.metric(label="Total Energy Capacity", value=f"{total_energy_capacity:,.2f} MW")

    ### Graphs
    fig1=px.sunburst(df_total,path=['Entity','country_long'],values='capacity_mw',color="capacity_mw",labels={'Entity':"Continent","country_long":"Country","capacity_mw":"Capacity (MegaWatt/Hour)"},title="Total Energy Capacity (MegaWatt/Hour)")
    fig2=px.bar(df_capacity_per_country,x=df_capacity_per_country['country_long'],y=df_capacity_per_country['capacity_mw'],labels={'capacity_mw':'Capacity (MegaWatt per Hour)',
                                                                                                                                    'country_long':'Country'},title='Energy Capacity (MegaWatt/Hour) Per Country')
    fig1.update_layout(height=500,showlegend=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)

    col1,col2=st.columns(2)
    with col1:
        st.subheader('Energy Capacity (MegaWatt/Hour) by Continent')
        df_capacity_per_continent=filtered_power_plants.groupby('Entity').agg({'capacity_mw':'sum'}).sort_values(by='capacity_mw',ascending=False).reset_index()
        fig3=px.bar(df_capacity_per_continent,x=df_capacity_per_continent['Entity'],y=df_capacity_per_continent['capacity_mw'],labels={'capacity_mw':'Capacity (MegaWatt per Hour)','Entity':'Continent'},title='Capacity (MegaWatt/Hour) Per Continent')
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.subheader('Energy Capacity (MegaWatt/Hour) by Continent')
        df_capacity_per_continent=filtered_power_plants.groupby('Entity').agg({'capacity_mw':'sum'}).sort_values(by='capacity_mw',ascending=False).reset_index()
        fig4 = px.funnel(df_capacity_per_continent, x='capacity_mw', y='Entity',labels={'capacity_mw':"Capacity (MegaWatt/Hour)","Entity":"Continent"})
        st.plotly_chart(fig4, use_container_width=True)

    # Create a bar chart using Plotly Express
    
    st.subheader('Energy Capacity (MegaWatt/Hour) by Fuel Type per Continent ')
   
    capacity_per_country_fuel = filtered_power_plants.groupby(['Entity', 'energy_type'])['capacity_mw'].sum().unstack(fill_value=0)

    fuel_types = ['Fossil Fuels', 'Nuclear', 'Other', 'Renewables']
    fuel_types_available = [fuel for fuel in fuel_types if fuel in capacity_per_country_fuel.columns]

    fig5 = px.bar(
        capacity_per_country_fuel.reset_index(), 
        x='Entity', 
        y=fuel_types_available,  # Only use the available fuel types
        labels={
            'Entity': 'Continent',
            'value': 'Total Capacity (MW)',
            'variable': 'Fuel Type'
        },
        title='Continent Capacity per Type of Primary Fuel'
        )                                                                                                                
    st.plotly_chart(fig5, use_container_width=True)

elif page=="Power Plants & Fuel Usage":
    st.title('Power Plants & Fuel Usage')
    image_path = r'background_12.06.33_PM.jpg'
    image = Image.open(image_path)


    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()


    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('data:image/jpeg;base64,{img_str}');
            background-size: cover;
            background-position: center;
        }}
        </style>
        """, unsafe_allow_html=True)
    Continent = st.sidebar.multiselect("Continent:", df_global_power_plants["Entity"].unique())

    #Function to filter all graphs by continent (Entity column) else return full graph
    def filter_by_continent(df, continents):
        if continents:
            return df[df["Entity"].isin(continents)]
        else:
            return df

    filtered_power_plants = filter_by_continent(df_global_power_plants, Continent)
    filtered_energy_consumption = filter_by_continent(df_energy_consumption, Continent)
    filtered_elec_production = filter_by_continent(df_elec_production, Continent)
    filtered_emissions = filter_by_continent(df_emissions, Continent)

    df_power_plants_per_country = df_global_power_plants['country_long'].value_counts().reset_index().head(20)
    df_power_plants_per_continent = filtered_power_plants['Entity'].value_counts().reset_index()
    st.title('Number of Power Plants per Country')
    fig1=px.bar(df_power_plants_per_country,x=df_power_plants_per_country['country_long'],y=df_power_plants_per_country['count'],labels={'count':'Number of Powerplants','country_long':'Country'},title='Top 20 Countries by Number of Power Plants')
    st.plotly_chart(fig1, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.title('Number of Powerplants per Continent Pie Chart')
        fig2=px.pie(df_power_plants_per_continent,values='count',names='Entity',labels={'count':'Number of Powerplants','Entity':'Continent'},title='Number of Power Plants per Continent')
        st.plotly_chart(fig2, use_container_width=True)
        

    with col2:
        st.title('Number of Powerplants per Continent Bar Plot')
        fig3=px.bar(df_power_plants_per_continent,x=df_power_plants_per_continent['Entity'],y=df_power_plants_per_continent['count'],labels={'count':'Number of Powerplants','Entity':'Continent'},title='Number of Power Plants per Continent')
        st.plotly_chart(fig3, use_container_width=True)
    
    ### ***Fuels by Continent
    top_5_fuels_by_region = filtered_power_plants.groupby('Entity')['energy_type'].value_counts().groupby(level=0).head(5)


    top_5_fuels_by_region_df = top_5_fuels_by_region.reset_index(name='Fuel Usage Count')


    top_5_fuels_by_region_df.columns = ['Entity', 'Primary_Fuel', 'Fuel Usage Count']


    fuel_options = top_5_fuels_by_region_df['Primary_Fuel'].unique()  # Get unique fuel types
    selected_fuels = st.multiselect('Select Fuels to Display', fuel_options)

    # If no fuels are selected, display the whole dataset
    if not selected_fuels:
        filtered_df = top_5_fuels_by_region_df
    else:
        # Filter the DataFrame based on selected fuels
        filtered_df = top_5_fuels_by_region_df[top_5_fuels_by_region_df['Primary_Fuel'].isin(selected_fuels)]

    # Create a bar chart using Plotly Express
    fig11 = px.bar(filtered_df,
                   x='Entity', 
                   y='Fuel Usage Count', 
                   color='Primary_Fuel', 
                   title='Fuel Usage by Continent')

    fig11.update_layout(
        xaxis_title='Continent'
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig11, use_container_width=True)
elif page=="Investment Opportunities":
    st.title("Investment Opportunities")
    image_path = r'background_12.06.33_PM.jpg'
    image = Image.open(image_path)


    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()


    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('data:image/jpeg;base64,{img_str}');
            background-size: cover;
            background-position: center;
        }}
        </style>
        """, unsafe_allow_html=True)
    Continent = st.multiselect("Select Continents to Display:", df_emissions["Entity"].unique())

    #Function to filter all graphs by continent (Entity column) else return full graph
    def filter_by_continent(df, continents):
        if continents:
            return df[df["Entity"].isin(continents)]
        else:
            return df

    filtered_emissions = filter_by_continent(df_emissions, Continent)
    fig1 = px.line(filtered_emissions,x='Year',y='Annual CO₂ emissions',color='Entity',title='Trends in Annual CO₂ Emissions by Continent',labels={'Year': 'Year','Annual CO₂ emissions': 'CO2 Emissions (Millions)','Entity': 'Continent'})
    st.plotly_chart(fig1,use_container_width=True)
    col1,col2=st.columns(2)

    with col1:
        #Filter out rows with NaN values in latitude or longitude
        valid_data = df_minerals_uranium.dropna(subset=['latitude', 'longitude'])

        #Initialize the map centered around the approximate midpoint of the data
        map_center = [valid_data['latitude'].mean(), valid_data['longitude'].mean()]
        mineral_map = folium.Map(location=map_center, zoom_start=2, tiles="CartoDB positron")

        #Add marker clustering
        marker_cluster = MarkerCluster().add_to(mineral_map)

        #Add points to the map
        for idx, row in valid_data.iterrows():
            popup_text = f"Site: {row['site_name']}<br>Country: {row['country']}"
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=popup_text,
                icon=folium.Icon(color='blue', icon='info-sign')  # Customize icon color/style
            ).add_to(marker_cluster)

        #Render the map in Streamlit
        st.title("Uranium Mines Map")
        st.components.v1.html(mineral_map._repr_html_(), height=500,width=600) 



    with col2:
        valid_earthquakes = df_earthquakes.dropna(subset=["latitude", "longitude"])
        map_center = [-35.0, -40.0]
        earthquake_map = folium.Map(location=map_center, zoom_start=2, tiles="CartoDB positron")

        marker_cluster = MarkerCluster().add_to(earthquake_map)

        for idx, row in valid_earthquakes.iterrows():
            popup_text = (
                f"Location: {row['place']}<br>"
                f"Magnitude: {row['mag']}<br>"
                f"Depth: {row['depth']} km<br>"
                f"Time: {row['time']}"
            )
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=popup_text,
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(marker_cluster)
        st.title("Earthquakes Distribution Map in South America")
        st.components.v1.html(
        f"""
        <div style="width: 800px; height: 400px;">
            {earthquake_map._repr_html_()}
        </div>
        """,
        height=400,width=600)



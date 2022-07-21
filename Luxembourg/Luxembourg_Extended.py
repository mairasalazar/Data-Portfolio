#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px 
import os.path
import streamlit as st
from plotly.graph_objects import Layout

st.set_page_config(layout="wide", page_title="Luxembourg Real Estate", page_icon=":house:")
# Use treat_luxcity to clean issues identified through previous exploration, such as use of asterisk to symbolize NA values, data types that didn't match (numbers as strings, for example) and spelling errors.


def treat_luxcity(df):
    """
    Clean up dataframes with data on quarters of Luxembourg City.

    This function replaces '*' characters with NA values,
    adjusts datatypes and prints summary & description of
    the information contained in dataframe.

    Parameters
    ----------
    df : dataframe
        Unclean dataframe.

    Returns
    -------
    dataframe
        Cleaned up dataframe.
    """
    df.replace("*", np.nan, inplace = True)
    df.iloc[:, 0] = df.iloc[:, 0].astype("str")
    df.iloc[:, 2] = df.iloc[:, 2].astype("float64")
    df.iloc[:, 3] = df.iloc[:, 3].astype("float64")
    df.rename(columns = {"Number of offers": "offers"}, inplace = True)
    df.iloc[:, 0].replace("Mülhenbach", "Mühlenbach", inplace = True) # Correct wrong spelling
    return df


def treat_country(dataframe):
    """
    Clean up dataframes with data on communes of Luxembourg.

    This function separates the dataframe into two: one for
    constructed apartments, the other for apartments under 
    contruction. It also replaces '*' characters with NA
    values, separates price range into minimal and maximal
    prices, adjusts datatypes and prints summary & description
    of the information contained in each dataframe.

    Parameters
    ----------
    df : dataframe
        Unclean dataframe.

    Returns
    -------
    treated[0] : dataframe
        Cleaned up dataframe for constructed apartments.
    treated[1] : dataframe
        Cleaned up dataframe for apartments in construction.
    """
    columns = list(dataframe.columns)
    columns_constructed = columns[0:4] + [columns[7]]
    columns_constructing = [columns[0]] + columns[4:]
    constructed = dataframe[columns_constructed]
    constructing = dataframe[columns_constructing]
    country_listing = [constructed, constructing]
    treated = []
    for df in country_listing:
        df.rename(columns = df.iloc[0], inplace = True)
        df = df.drop(df.index[0]).reset_index(drop=True)
        df.replace("*", np.nan, inplace = True)
        df[['Min price per squared meter in €', 'Max price per squared meter in €']] = df['Price range for price per squared meter'].str.split(' - ', expand=True)
        df.drop(['Price range for price per squared meter'], axis = 1, inplace = True)
        df.iloc[:, 0].replace("Kaerjeng", "Käerjeng", inplace = True) # Correct wrong spelling
        df.rename(columns = {"Number of sales": "sales"}, inplace = True)
        df.iloc[:, 0] = df.iloc[:, 0].astype('str')
        df.iloc[:, 2] = df.iloc[:, 2].astype('float64')
        df.iloc[:, 3] = df.iloc[:, 3].astype('int64')
        df.iloc[:, 4] = df.iloc[:, 4].astype('str').apply(lambda x: x.translate({ord(' '): None, ord('€'): None})).astype("float64")
        df.iloc[:, 5] = df.iloc[:, 5].astype('str').apply(lambda x: x.translate({ord(' '): None, ord('€'): None})).astype("float64")
        df.iloc[:, 3] = df.iloc[:, 3].astype('int64')
        treated.append(df)
    return treated[0], treated[1]
    


# Load data on prices


# Load data on population
total_population = pd.read_csv("./Resources/evolution_total_population.csv")
migration = pd.read_csv("./Resources/migration_population_canton_municipality.csv")
population_canton_mun = pd.read_csv("./Resources/population_canton_municipality.csv")
population_density = pd.read_csv("./Resources/population_density_canton_municipality.csv")

# Load lending data
lending = pd.read_csv("./Resources/lending_purchase_houses_millionsEUR.csv")

# Load Finished Buildings data
buildings = pd.read_csv("./Resources/finished-buildings.csv")

# ### Treat and analyse prices

apart_sale_city = treat_luxcity(apart_sale_luxcity)
apart_rent_city = treat_luxcity(apart_rent_luxcity)
house_sale_city = treat_luxcity(house_sale_luxcity)

# Decided to separate the data on apartment sales in the country into two dataframes
constructed_apart_sale, constructing_apart_sale = treat_country(apart_sale_luxcountry)

# ### Treat and analyse population

total_population = total_population.iloc[:, [1, 3, 4]]
total_population.rename(columns = {'SPECIFICATION: Specification':'population_type', 
                                   'TIME_PERIOD: Time period':'year', 
                                   'OBS_VALUE':'population'}, inplace = True)
total_population = total_population.loc[total_population.year.between(2009,2021)].sort_values(by='year').reset_index(drop=True)
total_population = total_population.reindex(columns=['year', 'population_type','population'])
total_population['population_type'] = total_population['population_type'].str.split(None, 1).str[1]

total_population.groupby('population_type').population.describe()


migration = migration.iloc[:, [1, 2, 4, 5]]
migration.rename(columns = {'POP_MOVEMENT: Population Movement':'movement',
                                   'SPECIFICATION: Specification': 'location',
                                   'TIME_PERIOD: Time period':'year', 
                                   'OBS_VALUE':'migration'}, inplace = True)
migration = migration.loc[migration.year.between(2009,2021)].sort_values(by='year').reset_index(drop=True)
migration = migration.reindex(columns=['year', 'movement','location', 'migration'])
migration['movement'] = migration['movement'].str.split(None, 1).str[1]
migration['location'] = migration['location'].str.split(None, 1).str[1]
migration['location'].replace(["Luxembourg", "Pétange", "Préizerdaul", "Rosport - Mompach"], 
                              ["Luxembourg City", "Petange", "Preizerdaul", "Rosport-Mompach"], inplace = True) # Correct wrong spelling
migration = migration[~migration.location.str.startswith('Canton')]

net_migration = migration[migration['movement']=='Net migration']

population_canton_mun = population_canton_mun.iloc[:, [2, 3, 4]]
population_canton_mun.rename(columns = {'SPECIFICATION: Specification': 'location',
                            'TIME_PERIOD: Time period':'year', 
                            'OBS_VALUE':'population'}, inplace = True)
population_canton_mun = population_canton_mun.loc[
    population_canton_mun.year.between(2009,2021)
].sort_values(by='year').reset_index(drop=True)
population_canton_mun = population_canton_mun.reindex(columns=['year', 'location', 'population'])
population_canton_mun['location'] = population_canton_mun['location'].str.split(None, 1).str[1]
population_canton_mun['location'].replace(["Luxembourg", "Pétange", "Préizerdaul", "Rosport - Mompach"], 
                              ["Luxembourg City", "Petange", "Preizerdaul", "Rosport-Mompach"], inplace = True) # Correct wrong spelling
population_canton_mun = population_canton_mun[~population_canton_mun.location.str.startswith('Canton')]

population_density = population_density.iloc[:, [1, 3, 4]]
population_density.rename(columns = {'SPECIFICATION: Specification': 'location',
                            'TIME_PERIOD: Time period':'year', 
                            'OBS_VALUE':'population_density'}, inplace = True)
population_density = population_density.loc[population_density.year.between(2009,2021)].sort_values(
    by='year').reset_index(drop=True)
population_density = population_density.reindex(columns=['year', 'location', 'population_density'])
population_density['location'] = population_density['location'].str.split(None, 1).str[1]
population_density['location'].replace(["Luxembourg", "Pétange", "Préizerdaul", "Rosport - Mompach"], 
                              ["Luxembourg City", "Petange", "Preizerdaul", "Rosport-Mompach"], inplace = True) # Correct wrong spelling
population_density = population_density[~population_density.location.str.startswith('Canton')]

lending = lending.iloc[:, [1, 3, 4]]
lending.rename(columns = {'SPECIFICATION: Specification': 'lender',
                            'TIME_PERIOD: Time period':'year', 
                            'OBS_VALUE':'lending_million_EUR'}, inplace = True)
lending = lending.loc[lending.year.between(2009,2021)].sort_values(
    by='year').reset_index(drop=True)
lending = lending.reindex(columns=['year', 'lender', 'lending_million_EUR'])
lending['lender'] = lending['lender'].str.split(None, 1).str[1]

type_to_keep = ['One-dwelling residental buildings', 'Week-end houses', 
                'Two and more dwelling residental buildings', 'Semi residential buildings']
buildings = buildings.iloc[:, [1, 2, 4, 5]]
buildings.rename(columns = {'BUILDINGS: Buildings':'buildings',
                            'SPECIFICATION: Specification': 'type',
                            'TIME_PERIOD: Time period':'year', 
                            'OBS_VALUE':'number'}, inplace = True)
buildings = buildings.loc[buildings.year.between(2009,2021)].sort_values(
    by='year').reset_index(drop=True)
buildings = buildings.reindex(columns=['year', 'buildings', 'type', 'number'])
buildings['buildings'] = buildings['buildings'].str.split(None, 1).str[1]
buildings['type'] = buildings['type'].str.split(None, 1).str[1]
buildings = buildings.loc[(buildings.type.isin(type_to_keep)) & (buildings.buildings == 'Number of dwellings')]

total_buildings = buildings.groupby(by=['year']).number.sum().to_frame()
total_buildings.reset_index(inplace = True)

# ## Rankings

# ### Prices

# Combine both dataframes vertically, in order to find lowest and highest prices per squared meter
luxcountry = [constructed_apart_sale, constructing_apart_sale]
luxcountry_df = pd.concat(luxcountry)

# Communes with lowest average prices per squared meter and communes with highest average prices per squared meter


# Offers for apartments for rent, apartments for sale and houses for sale in Luxembourg City
luxcity = [apart_sale_city, apart_rent_city, house_sale_city]
city_offers = []
for df in luxcity:
    df1 = df.groupby("Year").offers.sum().to_frame()
    city_offers.append(df1)
apart_s_offers_city, apart_r_offers_city, house_s_offers_city = city_offers[0], city_offers[1], city_offers[2]

# Total sales of apartments (constructed and in construction) in the country
total_sales = luxcountry_df.copy().rename(columns = {"Number of sales": "sales"})
total_sales = total_sales.groupby("Year").sales.sum().to_frame()

# Sales of apartments in Luxembourg City
sales_apart_luxcity = luxcountry_df.copy().rename(columns = {"Number of sales": "sales"})
sales_apart_luxcity = sales_apart_luxcity.loc[sales_apart_luxcity['Commune'] == 'Luxembourg City']
sales_apart_luxcity = sales_apart_luxcity.groupby(["Year", 'Commune']).sales.sum().to_frame()

year_list = list(apart_s_offers_city.index.values)

# Number of sales of constructed apartments and apartments under construction 
luxcountry_sales = []
for df in luxcountry:
    df1 = df.copy().rename(columns = {"Number of sales": "sales"})
    df1 = df1.groupby("Year").sales.sum().to_frame()
    luxcountry_sales.append(df1)
apart_sales_constructed, apart_sales_constructing = luxcountry_sales[0], luxcountry_sales[1]

# Number of sales of constructed apartments vs apartments under construction
fig = go.Figure()
fig.add_trace(go.Bar(
    x = year_list,
    y = apart_sales_constructed.sales,
    name = 'Constructed apartments',
    marker_color = 'lightslategray'
))

fig.add_trace(go.Bar(
    x = year_list,
    y = apart_sales_constructing.sales,
    name = 'Apartments under construction',
    marker_color = 'lightskyblue'
))

fig.update_layout(
    title={
        'text': "Number of sales of apartments in Luxembourg (2009-2021)",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Year",
    yaxis_title="Number of sales",
    legend_title="Type of apartment",
    barmode='group',
)
fig.update_xaxes(nticks=15)


apart_s_city = apart_sale_city.loc[apart_sale_city['Quarter']=='Luxembourg City'].rename(
                                                        columns={"Average announced price in €":"avg_price", 
                                                        "Average announced price per squared meter in €":"avg_price_sqm"})
apart_r_city = apart_rent_city.loc[apart_rent_city['Quarter']=='Luxembourg City'].rename(
                                                        columns={"Average announced price in €":"avg_price", 
                                                        "Average announced price per squared meter in €":"avg_price_sqm"})
house_s_city = house_sale_city.loc[house_sale_city['Quarter']=='Luxembourg City'].rename(
                                                        columns={"Average announced price in €":"avg_price", 
                                                        "Average announced price per squared meter in €":"avg_price_sqm"})


# Average prices of apartments for sale vs houses for sale. 
# This might partially explain why the demand for apartments is much larger that the demand for houses, beyond the difference
# in the number of existing apartments when compared to existing houses. 
avg_price_city = go.Figure()
avg_price_city.add_trace(go.Scatter(x=year_list,
                    y=apart_s_city.avg_price,
                    mode='lines+markers',
                    name = 'Apartment average price',
                    marker_color = 'indianred'))
avg_price_city.add_trace(go.Scatter(x=year_list,
                    y=house_s_city.avg_price,
                    mode='lines+markers',
                    name = 'House average price',
                    marker_color = 'lightsalmon'))

avg_price_city.update_layout(
    title={
        'text': "Average price of apartments and houses for sale in Luxembourg City (2009-2021)",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Year",
    yaxis_title="Average Announced Price",
    barmode='group',
)

avg_price_city.update_xaxes(nticks=15)

# Percentual change in average announced prices for Luxembourg City
apart_r_city['Pct_change_average_price'] = apart_r_city.iloc[:,2].pct_change()
apart_s_city['Pct_change_average_price'] = apart_s_city.iloc[:,2].pct_change()


# Percentage change in average announced prices
fig = go.Figure()
fig.add_trace(go.Scatter(x=year_list,
                    y=apart_s_city['Pct_change_average_price'],
                    mode='lines+markers',
                    name = 'Apartments for sale',
                    marker_color = 'indianred'))
fig.add_trace(go.Scatter(x=year_list,
                    y = apart_r_city['Pct_change_average_price'],
                    mode='lines+markers',
                    name = 'Apartments for rent',
                    marker_color = 'burlywood'))

fig.update_layout(
    title={
        'text': "Percentage change in average announced prices for Luxembourg City (2009 - 2021)",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Year",
    yaxis_title="Percentage Change",
    legend_title="Type of apartment",
    barmode='group',
)

fig.update_xaxes(nticks=14)

# Price-to-Rent Ratio
luxcity_aparts = pd.concat([apart_s_city.set_index('Year').iloc[:, 2], apart_r_city.set_index('Year').iloc[:, 2]], axis=1)
luxcity_aparts['price_to_rent'] = luxcity_aparts.iloc[:, 0] / (luxcity_aparts.iloc[:, 1] * 12)

fig = go.Figure()
fig.add_trace(go.Scatter(x=year_list,
                    y=luxcity_aparts.price_to_rent,
                    mode='lines+markers',
                    name = 'Price-to-Rent Ratio',
                    marker_color = 'steelblue'))
fig.update_layout(
    title={
        'text': "Price-to-rent ratio for Luxembourg City (2009 - 2021)",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Year",
    yaxis_title="Price-to-Rent Ratio",
    barmode='group',
)
fig.update_xaxes(nticks=15)

# Number of offers and Price-to-Rent ratio
offer_ratio = go.Figure()
trace1 = go.Bar(
    x = year_list,
    y = apart_r_offers_city.offers,
    name = 'Apartments for rent',
    marker_color = 'burlywood', opacity=0.9
)
trace2 = go.Bar(
    x = year_list,
    y = apart_s_offers_city.offers,
    name = 'Apartments for sale',
    marker_color = 'indianred', opacity=0.9
)
trace3 = go.Bar(
    x = year_list,
    y = house_s_offers_city.offers,
    name = 'Houses for sale',
    marker_color = 'lightsalmon', opacity=0.9
)
trace4 = go.Scatter(x=year_list,
                    y=luxcity_aparts.price_to_rent,
                    mode='lines+markers',
                    name = 'Price-to-Rent Ratio',
                    marker_color = 'steelblue', yaxis = 'y2')


offer_ratio = make_subplots(specs=[[{"secondary_y": True}]])

offer_ratio.add_trace(trace1)
offer_ratio.add_trace(trace2)
offer_ratio.add_trace(trace3)
offer_ratio.add_trace(trace4, secondary_y=True)

offer_ratio.update_layout(
    title={
        'text': "Number of offers and price-to-rent ratio for Luxembourg City (2009-2021)",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Year",
    yaxis_title="Number of offers",
    barmode='group',
)

offer_ratio.update_yaxes(title_text="Price-to-Rent Ratio", secondary_y = True)
offer_ratio.update_xaxes(nticks=15)

# Average registered price per squared meter for apartments - National average
luxcountry_mean =  []
for df in luxcountry:
    df_mean = df.rename(columns = {"Average registered price per squared meter in €": "avg_price_sqm"})
    df_mean = df_mean[df_mean['Commune'] == 'National Average']
    
    luxcountry_mean.append(df_mean)
apart_constructed_mean, apart_constructing_mean = luxcountry_mean[0], luxcountry_mean[1]

# Prices for apartments constructed and apartments under construction, compared to number of sales for each type
sales_price_country = go.Figure()
trace1 = go.Bar(
    x = year_list,
    y = apart_sales_constructed.sales,
    name = 'Sales - constructed apartments',
    marker_color = 'indianred', opacity=0.6
)
trace2 = go.Bar(
    x = year_list,
    y = apart_sales_constructing.sales,
    name = 'Sales - future apartments',
    marker_color = 'lightsalmon', opacity=0.6
)
trace3 = go.Scatter(x=year_list,
                    y=apart_constructed_mean.avg_price_sqm,
                    mode='lines+markers',
                    name = 'Price - constructed apartments',
                    marker_color = 'indianred', yaxis='y2'
)                    
trace4 = go.Scatter(x=year_list,
                    y = apart_constructing_mean.avg_price_sqm,
                    mode='lines+markers',
                    name = 'Price - future apartments',
                    marker_color = 'lightsalmon', 
                    yaxis='y2')

sales_price_country = make_subplots(specs=[[{"secondary_y": True}]])

sales_price_country.add_trace(trace1)
sales_price_country.add_trace(trace2)
sales_price_country.add_trace(trace3,secondary_y=True)
sales_price_country.add_trace(trace4,secondary_y=True)

sales_price_country.update_layout(
    title={
        'text': "Average prices per squared meter and number of sales for apartments in Luxembourg (2009-2021)",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Year",
    yaxis_title="Number of sales",
    barmode='group',
)

sales_price_country.update_yaxes(title_text="Average prices per squared meter", secondary_y = True)
sales_price_country.update_xaxes(nticks=15)

# Average registered prices per squared meter of constructed apartments in Luxembourg city
# vs average registered prices per squared meter of apartments under construction in Luxembourg city
# vs average announced prices of apartments in Luxembourg city
fig = go.Figure()
fig.add_trace(go.Bar(
    x = year_list,
    y = apart_s_city.avg_price_sqm,
    name = 'Announced prices',
    marker_color = 'indianred'
))
fig.add_trace(go.Bar(
    x = year_list,
    y = apart_constructed_mean.avg_price_sqm,
    name = 'Registered prices - constructed apartments',
    marker_color = 'lightslategrey'
))
fig.add_trace(go.Bar(
    x = year_list,
    y = apart_constructing_mean.avg_price_sqm,
    name = 'Registered prices - future apartments',
    marker_color = 'lightskyblue'
))

fig.update_layout(
    title={
        'text': "Average announced and registered prices per squared meter in Luxembourg City (2009-2021)",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Year",
    yaxis_title="Prices",
    barmode='group',
)
fig.update_xaxes(nticks=15)


# Prices for apartments constructed and apartments under construction, compared to number of sales for each type
fig=go.Figure()
trace1 = go.Bar(
    x = year_list,
    y = apart_s_offers_city.offers,
    name = 'Offers - apartments',
    marker_color = 'indianred', opacity=0.7
)

trace2 = go.Bar(
    x = year_list,
    y = house_s_offers_city.offers,
    name = 'Offers - houses',
    marker_color = 'lightsalmon', opacity=0.7
)

trace3 = go.Scatter(x=year_list,
                    y= apart_s_city.avg_price,
                    mode='lines+markers',
                    name = 'Average price - apartments',
                    marker_color = 'indianred', yaxis='y2')
                    
trace4 = go.Scatter(x=year_list,
                    y = house_s_city.avg_price,
                    mode='lines+markers',
                    name = 'Average price - houses',
                    marker_color = 'lightsalmon', 
                    yaxis='y2')

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(trace1)
fig.add_trace(trace2)
fig.add_trace(trace3,secondary_y=True)
fig.add_trace(trace4,secondary_y=True)

fig.update_layout(
    title={
        'text': "Average prices and number of offers for apartments and houses in Luxembourg City (2009-2021)",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Year",
    yaxis_title="Number of offers",
    barmode='group',
)

fig.update_yaxes(title_text="Average prices", secondary_y = True)
fig.update_xaxes(nticks=15)

# Sum number of sales and average prices for constructed and future apartments
combined_aparts = constructed_apart_sale.drop(columns=["Min price per squared meter in €",
                                                               "Max price per squared meter in €"]).rename(
    columns={"Average registered price per squared meter in €":"avg_price_sqm_1", "sales":"sales_1"})
combined_aparts["avg_price_sqm_2"] = constructing_apart_sale["Average registered price per squared meter in €"]
combined_aparts["sales_2"] = constructing_apart_sale["sales"]
combined_aparts["avg_price_sqm"] = combined_aparts[['avg_price_sqm_1', 'avg_price_sqm_2']].mean(axis=1)
combined_aparts["sum_sales"] = combined_aparts[['sales_1', 'sales_2']].sum(axis=1)
combined_aparts = combined_aparts.sort_values(['Commune', "Year"], ascending = [True, True])
national = combined_aparts.loc[combined_aparts['Commune'] == "National Average"]
combined_aparts = combined_aparts.drop(list(national.index.values))

remove = ["National Average", "Luxembourg City"]
constructed_apart_salegraph = constructed_apart_sale[constructed_apart_sale['Commune'].isin(remove) == False]

# Total sales per Commune
fig = px.scatter(combined_aparts, x='Year', y="sum_sales", color='Commune', opacity=0.8,
                labels={
                     "sum_sales": "Number of sales",
                 }
)
fig.update_layout(title_text="Total number of sales per commune in Luxembourg (2009 - 2021)", title_x=0.5)

# Get average price per square meter for sold apartments in each commune, as well as national average
average_price_apartments = constructed_apart_sale.drop(columns=["Min price per squared meter in €",
                                                               "Max price per squared meter in €",
                                                               "sales"]).rename(
    columns={"Average registered price per squared meter in €":"avg_price_sqm_1"})
average_price_apartments["avg_price_sqm_2"] = constructing_apart_sale["Average registered price per squared meter in €"]
average_price_apartments["avg_price_sqm"] = average_price_apartments[['avg_price_sqm_1', 'avg_price_sqm_2']].mean(axis=1)
average_price_apartments.drop(columns=['avg_price_sqm_1', 'avg_price_sqm_2'], inplace = True)
average_price_apartments = average_price_apartments.sort_values(['Commune', "Year"],
              ascending = [True, True])
national_average = average_price_apartments.loc[average_price_apartments['Commune'] == "National Average"]
average_price_apartments = average_price_apartments.drop(list(national_average.index.values))

# Growth evolution of prices per squared meter for sold apartments in each commune, with national average
fig = px.scatter(average_price_apartments, x='Year', y=average_price_apartments.avg_price_sqm, color='Commune', opacity=0.8)
fig.add_trace(go.Scatter(x=year_list,
                    y=national_average.avg_price_sqm,
                    mode='lines+markers',
                    name = 'Calculated National Average',
                    marker_color = 'steelblue')
)
fig.update_layout(
    title={
        'text': "Growth evolution of prices per squared meter for sold apartments in each commune in Luxembourg (2009-2021)",
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Year",
    yaxis_title="Average price/m2",
    barmode='group',
)

fig.update_xaxes(nticks=15)

# Year on year growth on number of offers per quarter
sum_offers = apart_rent_city.drop(columns=["Average announced rent in €", "Average announced rent per squared meter in €"])
sum_offers["offers2"], sum_offers["offers3"] = apart_sale_city["offers"], house_sale_city["offers"]
sum_offers["total_offers"] = sum_offers[["offers", "offers2", "offers3"]].sum(axis=1)
sum_offers.drop(columns=["offers", "offers2", "offers3"], inplace = True)
remove = sum_offers.loc[sum_offers['Quarter'].isin(["National Average", "Luxembourg City"])].index.values.tolist()
sum_offers = sum_offers.drop(remove)
sum_offers['yearly_growth_offers'] = sum_offers.groupby("Quarter").total_offers.pct_change()

highest_growth = sum_offers.copy()
highest_growth['pct_change_period'] = highest_growth.groupby("Quarter").total_offers.pct_change(12)
highest_growth = highest_growth.sort_values('pct_change_period', ascending = False)
highest_growth.head(5)

# Year on year growth of offers per quarter 
fig = px.line(sum_offers, x='Year', y=sum_offers.yearly_growth_offers, color='Quarter')
fig.update_layout(
    title={
        'text': "Year on year growth of number of offers per quarter in Luxembourg City (2009-2021)",
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Year",
    yaxis_title="Percentage change in number of offers",
    barmode='group',
)

fig.update_xaxes(nticks=15)


px.bar(sum_offers, x="Quarter", y=sum_offers.yearly_growth_offers, color="Quarter",
  animation_frame="Year", animation_group="Quarter", hover_name="Quarter", range_y=[0,4.5])


# Median Multiple
median_house_price = 1112500
median_disp_income = 5454*12
median_multiple = median_house_price/median_disp_income


# ### Population

communes = ['Kiischpelt', 'Boulaide', 'Lac de la Haute-Sûre', 'Wincrange', 'Putscheid', 'Larochette',
 'Saeul', 'Reisdorf', 'Grosbous', 'Petange', 'Esch-sur-Alzette', 'Differdange', 'Luxembourg City', 
 'Walferdange', 'Schifflange']

total_population_total = total_population.loc[total_population.population_type == 'Total population']
total_population_foreigners = total_population.loc[total_population.population_type == 'Foreigners']
total_population_lux = total_population.loc[total_population.population_type == 'Luxembourgers']
total_population_proportion = total_population.loc[total_population.population_type == 'Proportion of foreigners (in %)']

net_migration = migration.loc[migration.movement=='Net migration']
net_migration.groupby('location').migration.mean().sort_values()
net_migration_com = net_migration.loc[net_migration.location.isin(communes)].drop(['movement'], axis=1)
population_density_com = population_density.loc[population_density.location.isin(communes)]
combined = pd.merge(net_migration_com, population_density_com, how='outer', left_on = ['location', 'year'], right_on = ['location', 'year'])

total_population_total = total_population.loc[total_population.population_type == 'Total population']
net_migration_country = net_migration.loc[net_migration.location.str.startswith('Grand')]

# Number of offers and Price-to-Rent ratio
population_graph = go.Figure()
trace1 = go.Scatter(x=year_list,
                    y=total_population_total.population,
                    mode='lines+markers',
                    name = 'total population',
                    marker_color = 'indianred')

population_graph.add_trace(trace1)

population_graph.update_layout(
    title={
        'text': "Population in Luxembourg (2009-2021)",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Year",
    yaxis_title="Number of offers",
    barmode='group',
)

population_graph.update_yaxes(title_text="Population")
population_graph.update_xaxes(nticks=15)

migration_dwellings = go.Figure()
trace1 = go.Scatter(x=year_list,
                    y=net_migration_country.migration,
                    mode='lines+markers',
                    name = 'net migration',
                    marker_color = 'burlywood')
trace2 = go.Scatter(x=year_list,
                    y=total_buildings.number,
                    mode='lines+markers',
                    name = 'new dwellings',
                    marker_color = 'lightsalmon')
migration_dwellings.add_trace(trace1)
migration_dwellings.add_trace(trace2)
migration_dwellings.update_layout(
    title={
        'text': "Net migration and new dwellings in Luxembourg (2009-2021)",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Year",
    yaxis_title="Number of offers",
    barmode='group',
)

migration_dwellings.update_yaxes(title_text="Population and new dwellings")
migration_dwellings.update_xaxes(nticks=15)

pdl = set(population_density.location.to_list())
nml = set(net_migration.location.to_list())
all_communes = set(luxcountry_df.Commune.to_list())
set1 = pdl.intersection(nml)
result_set = set1.intersection(all_communes)
in_all = list(result_set)

country = luxcountry_df.loc[luxcountry_df.Commune.isin(in_all)]
density_country = population_density[population_density.location.isin(in_all)]
net_migration_country = net_migration[net_migration.location.isin(in_all)]

country = country[~country.index.duplicated(keep='first')]
country = country.rename(columns={'Average registered price per squared meter in €': 'avg_reg_price_sqrmeter',
                             'Min price per squared meter in €': 'min_price_sqrmeter',
                             'Max price per squared meter in €': 'max_price_sqrmeter', 'Year': 'year', 'Commune':'location'
                            })

pop_mig = pd.merge(density_country, net_migration_country, how='outer', left_on = ['location', 'year'], right_on = ['location', 'year'])
pop_mig_sales = pd.merge(pop_mig, country, how='outer', left_on = ['location', 'year'], right_on = ['location', 'year'])
pop_mig_sales['sales'] = pop_mig_sales['sales'].fillna(0)
pop_mig_sales_graph = px.scatter(pop_mig_sales, x="sales", y="migration", animation_frame="year", animation_group="location",
           size="population_density", color="location", hover_name="location",
           log_x=False, size_max=25, range_x=[0,700], range_y=[-200,4500],
           category_orders={'location': np.sort(pop_mig_sales['location'].unique())})

pop_mig_sales_graph["layout"].pop("updatemenus") # drop animation buttons


pop_mig_sales_no_lux = pop_mig_sales[pop_mig_sales.location!='Luxembourg City']
pop_mig_sales_no_lux_graph = px.scatter(pop_mig_sales_no_lux, x="sales", y="migration", animation_frame="year", animation_group="location",
           size="population_density", color="location", hover_name="location",
           log_x=False, size_max=25, range_x=[0,360], range_y=[-200,950], 
           category_orders={'location': np.sort(pop_mig_sales_no_lux['location'].unique())})
pop_mig_sales_no_lux_graph["layout"].pop("updatemenus")

population_canton_mun_com = population_canton_mun.loc[population_canton_mun.location.isin(communes)]

population_commune = px.bar(population_canton_mun_com, x="year", y="population", color="location", title="Population by Commune")

fig = px.line(net_migration_com, x='year', y="migration", color='location',
                labels={
                     "location": "Commune",
                 }
)
fig.update_layout(title_text="Migration per commune in Luxembourg (2009 - 2021)", title_x=0.5)


fig2 = px.line(combined, x="year", y="population_density", color="location")
#fig2 = px.bar(population_density, x="year", y="population_density", col)
fig2.update_layout(title_text="Population density per commune in Luxembourg (2009 - 2021)", title_x=0.5)

combined_aparts_com = combined_aparts.loc[combined_aparts.Commune.isin(communes)]
fig = px.scatter(combined_aparts_com, x='Year', y="sum_sales", color='Commune', opacity=0.8,
                labels={
                     "sum_sales": "Number of sales",
                 }
)
fig.update_layout(title_text="Total number of sales per commune in Luxembourg (2009 - 2021)", title_x=0.5)

total_loans = lending.loc[lending.lender == 'Total loans']

fig = px.line(total_loans, x="year", y="lending_million_EUR", title="Total Loans for purchase of houses, in million EUR")

# **Conclusion**: We see that population continues to grow, and net migration is positive. As such, demand for appartments continue to grow. 
# Petange, Schifflange, Differdange, Wincrange, Walferdange seem promising in terms of positive migration and increase and sales, but population density not as high as Luxembourg City or Esch-sur-Alzette
# 
# Furthermore, lending for purchase of housings has increased dramatic, as has the number of offers. However, number of sales has been much more stable, indicating that demand far exceeds supply.

# ### Maps

# In[76]:

from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/luxembourg-communes.geojson') as response:
    communes = json.load(response)

commune_id_map = {}
for feature in communes["features"]:
    feature["id"] = feature["properties"]["cartodb_id"]
    commune_id_map[feature["properties"]["name"]] = feature["id"]

commune_list = list(commune_id_map.keys())


# #### Migration

df_migration = net_migration.groupby('location')['migration'].sum().to_frame().reset_index()
df_migration['location'].replace(["Luxembourg City", "Petange", "Preizerdaul"], 
                              ["Luxembourg", "Pétange", "Préizerdaul"], inplace = True)
diff = list(set(list(df_migration.location)) - set(commune_list))
diff2 = list(set(commune_list) - set(list(df_migration.location)))
for i in diff2:
    df_migration.loc[len(df_migration)] = [i, np.nan]
df_migration = df_migration.loc[~df_migration.location.isin(diff)]
df_migration["migration"].fillna(-100, inplace=True)
df_migration["id"] = df_migration["location"].apply(lambda x: commune_id_map[x])

layout = Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

migration_map = go.Figure(layout=layout)
migration_map.add_trace(go.Choropleth(locations = df_migration["id"], 
                            z = df_migration["migration"],
                            geojson=communes,
                            colorscale=[[0.0, "rgb(220,220,220)"],[0.0001, "rgb(220,220,220)"], 
                                        [0.0001, "rgb(155, 34, 38)"],
                [0.01, "rgb(155, 34, 38)"],
                [0.06, "rgb(187, 62, 3)"],
                [0.12, "rgb(202, 103, 2)"], [0.18, "rgb(238, 155, 0)"],
                [0.24, "rgb(233, 216, 166)"],[0.3, "rgb(148, 210, 189)"], [1.0, "rgb(10, 147, 150)"]],
                            hoverinfo=["location+z"],
                            name="Net migration"
))
migration_map.update_geos(fitbounds="locations", visible=False)
migration_map.update_layout(geo_bgcolor='rgba(0,0,0,0)')

# #### Population Density

df_density = population_density.groupby('location')['population_density'].mean().to_frame().reset_index()
df_density['location'].replace(["Luxembourg City", "Petange", "Preizerdaul"], 
                              ["Luxembourg", "Pétange", "Préizerdaul"], inplace = True)
diff = list(set(list(df_density.location)) - set(commune_list))
diff2 = list(set(commune_list) - set(list(df_density.location)))
for i in diff2:
    df_density.loc[len(df_density)] = [i, np.nan]
df_density = df_density.loc[~df_density.location.isin(diff)]
df_density["population_density"].fillna(-100, inplace=True)
df_density["id"] = df_density["location"].apply(lambda x: commune_id_map[x])

density_map = go.Figure()
density_map.add_trace(go.Choropleth(locations = df_density["id"], 
                            z = df_density["population_density"],
                            geojson=communes,
                            colorscale=[[0.0, "rgb(220,220,220)"],[0.0001, "rgb(220,220,220)"], 
                                        [0.0001, "rgb(155, 34, 38)"],
                [0.125, "rgb(155, 34, 38)"], [0.250, "rgb(174, 32, 18)"],
                [0.375, "rgb(187, 62, 3)"],
                [0.5, "rgb(202, 103, 2)"], [0.625, "rgb(238, 155, 0)"],
                [0.75, "rgb(233, 216, 166)"],[0.875, "rgb(148, 210, 189)"], [1.0, "rgb(10, 147, 150)"]],
                            hoverinfo=["location+z"],
                            name="Population density"
))
density_map.update_geos(fitbounds="locations", visible=False)
density_map.update_layout(geo_bgcolor='rgba(0,0,0,0)')
# #### Sales

df_sales = luxcountry_df.groupby('Commune')['sales'].sum().to_frame().reset_index()
df_sales['Commune'].replace(["Luxembourg City", "Petange", "Preizerdaul"], 
                              ["Luxembourg", "Pétange", "Préizerdaul"], inplace = True)
diff = list(set(list(df_sales.Commune)) - set(commune_list))
diff2 = list(set(commune_list) - set(list(df_sales.Commune)))
for i in diff2:
    df_density.loc[len(df_density)] = [i, np.nan]
df_sales = df_sales.loc[~df_sales.Commune.isin(diff)]
df_sales["sales"].fillna(-1000, inplace=True)
df_sales["id"] = df_sales["Commune"].apply(lambda x: commune_id_map[x])

sales_map = go.Figure(layout=layout)
sales_map.add_trace(go.Choropleth(locations = df_sales["id"],
                            z = df_sales["sales"],
                            geojson=communes,
                            colorscale=[[0.0, "rgb(220,220,220)"],[0.0001, "rgb(220,220,220)"], 
                                        [0.0001, "rgb(155, 34, 38)"],
                [0.01, "rgb(155, 34, 38)"],
                [0.06, "rgb(187, 62, 3)"],
                [0.12, "rgb(202, 103, 2)"], [0.18, "rgb(238, 155, 0)"],
                [0.24, "rgb(233, 216, 166)"],[0.3, "rgb(148, 210, 189)"], [1.0, "rgb(10, 147, 150)"]],
                            hoverinfo=["location+z"],
                            name="Sales"
))
sales_map.update_geos(fitbounds="locations", visible=False)
sales_map.update_layout(geo_bgcolor='rgba(0,0,0,0)')
# #### Prices


df_prices = luxcountry_df.groupby('Commune')['Average registered price per squared meter in €'].mean().to_frame().reset_index()
df_prices['Commune'].replace(["Luxembourg City", "Petange", "Preizerdaul"], 
                              ["Luxembourg", "Pétange", "Préizerdaul"], inplace = True)
diff = list(set(list(df_prices.Commune)) - set(commune_list))
df_prices = df_prices.loc[~df_prices.Commune.isin(diff)]
df_prices["Average registered price per squared meter in €"].fillna(-1000, inplace=True)
df_prices["id"] = df_prices["Commune"].apply(lambda x: commune_id_map[x])

prices_map = go.Figure()
prices_map.add_trace(go.Choropleth(locations = df_prices["id"],
                            z = df_prices["Average registered price per squared meter in €"],
                            geojson=communes,
                            colorscale=[[0.0, "rgb(220,220,220)"],[0.0001, "rgb(220,220,220)"], 
                                        [0.0001, "rgb(155, 34, 38)"],
                [0.125, "rgb(155, 34, 38)"], [0.250, "rgb(174, 32, 18)"],
                [0.375, "rgb(187, 62, 3)"],
                [0.5, "rgb(202, 103, 2)"], [0.625, "rgb(238, 155, 0)"],
                [0.75, "rgb(233, 216, 166)"],[0.875, "rgb(148, 210, 189)"], [1.0, "rgb(10, 147, 150)"]],
                            hoverinfo=["z"], hovertext = df_prices['Commune'],
                            name="Average registered price per squared meter in €",
                                   colorbar_title="Avg €/m2"
))
prices_map.update_geos(fitbounds="locations", visible=False)
prices_map.update_layout(geo_bgcolor='rgba(0,0,0,0)')
prices_map.update_layout(
    title={
        'text': "Average registered price per squared meter in € (2009-2021)",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})



# ## Streamlit

st.title("Real Estate in Luxembourg - State of Affairs")
col1_1, col1_2 = st.columns((1,1))

with st.container():
    with col1_1:
        show_lux = st.checkbox('Show Luxembourg City', value=True)
        if show_lux:
            st.plotly_chart(pop_mig_sales_graph, use_container_width=False, sharing="streamlit")
        else:
            st.plotly_chart(pop_mig_sales_no_lux_graph, use_container_width=False, sharing="streamlit")
    with col1_2:
        st.plotly_chart(prices_map, use_container_width=False)

col2_1, col2_2 = st.columns((1,1))
with st.container():
    with col2_1:
        st.header("The project")
        st.write('''The inspiration for this dashboard was the [Data Analysis competition](https://www.pwc.lu/en/careers/data-analytics-challenge-2022.html) and
        by PWC Luxembourg. The questions we aim to answer here are: I) What are the recent trends of the Real Estate Market in Luxembourg and
        II) Where to invest in Real Estate in Luxembourg?
        If this dashboard is something that interests you, feel free to check out the [Git repo](https://github.com/mairasalazar/Data-Portfolio).''')
    with col2_2:
        st.header("Where to invest in real estate in Luxembourg")
        st.write('''Differdange, Pedange, Dudelange and Sanem are promissing Communes. They have space for growth in terms of population
        density, are attractive places based on trends of net migration, and are still relatively affordable.''') 
        st.write('''However, it is worth pointing out that, based in the present analysis, affordability levels are low, prices are in general extremely high and potentially overvalued – in such case, market corrections are likely to happen in Luxembourg. As such, it might be worthwhile to wait for the implementation of policies that lead to an increase in supply. To be able to deal with the demand that continues to increase as migration to Luxembourg is still high, many more properties will be developed in the upcoming years. We can expect busy years for land developers and construction companies, specially if the government implements measures to increase the supply of housing.''')

st.header("Price and Sale evolution")

col3_1, col3_2 = st.columns((1,1))
with st.container():
    with col3_1:
        st.plotly_chart(sales_price_country, use_container_width=False, sharing="streamlit")
        st.write('''Until 2018, prices for both types of apartments were rising at a more or less stable rate. Prices increased more 
        rapidly for both since 2018. Finally, we can see that there are more fluctuations in the number of sales than on the prices, 
        indicating once more that supply is not meeting demand. 
        There are more fluctuations in the number of sales than on the prices, indicating once more that supply is not meeting demand.''')
    with col3_2:
        st.plotly_chart(offer_ratio, use_container_width=False, sharing="streamlit")
        st.write('''The Price-to-Rent Ratio is a good tool to see how the costs of purchasing a residential compare to the costs of 
        renting it. Values equal or above 21 are an indication that it is better to rent an appartment than to buy it, which is the 
        case in Luxembourg City.
        We can also see that the price-to-rent ratio has been increasingly steadily, as has the number of offers for renting apartments 
        over buying apartments. It was not always the case.''')

st.header('The main issue: demand far exceeds supply')

col4_1, col4_2 = st.columns((1,1))
with st.container():
    with col4_1:
        st.plotly_chart(migration_dwellings, use_container_width=False, sharing="streamlit")
        st.write("""Looking only at net migration, we see that Luxembourg's population has been growing by almost 2x the number
        of new dwellings (housing units) - another indicator that not enough is being done to match supply and demand.""")
    with col4_2:
        st.plotly_chart(population_commune, use_container_width=False, sharing="streamlit")
        st.write("""A closer look at how population has been growing in different communes. **Feel free to click in a commune in a 
        commune name in the legend to remove it from the graph, or double click to isolate it.**""")

with st.container():
    st.write(' ')
    st.write('''The demand for apartments and houses continue to increase steeply, and as a result, property prices continue to climb.
    The supply of properties in the country, however, has not grown at the same pace.

In this scenario, where demand already exceeds demand, a price ceiling would not be recommended. As such, the government could implement
 policies to increase the supply side of the market. Incentives to land developers and land owners, to ensure that available land is
  being transformed in property in the near future, can be an alternative. It can also be interesting to look at what are the current 
  regulations in terms of residential density (how high can apartments be, with how many units…) to develop alternative ways of
   increasing the number of residential units.

At the same time, distributing the population throughout the country is also important. As we can see in the graph, 
sales are highly concentrated in Luxembourg City, and communes have a much lower population density as of now. Policies to incentivise
 the purchase of houses and apartments in other areas of the country can help alleviate the pressure in the real estate market. 
 For this, it is important to focus in regions with good public transportation coverage and, in t he long term, potentially look into 
 improving transportation between regions. The rationale is to allow fast commutes for those not living in Luxembourg City, 
 increasing the attractiveness of other areas in the country. Potentially, tax benefits could be offered to new home owners outside 
 Luxembourg City. 
''')
# %%

#!/usr/bin/env python
# coding: utf-8


from sre_constants import OP_LOCALE_IGNORE
import country_converter as coco
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import calendar


def create_text(df, col):
    '''
    Returns a string with text of all rows of a certain column in a dateframe. 

            Parameters:
                    df (DataFrame): a dataframe with at least one column of type string
                    col (str): name of a column in df

            Returns:
                    text (str)
    '''
    text = " ".join(line for line in df[col].astype(str))
    return text


def countries(with_abbreviations=True):
    '''
    Returns a list of countries, with or without ISO 3 abbreviations. 

            Parameters:
                    with_abbreviations (boolean)

            Returns:
                    countries_list (list)
    '''
    if with_abbreviations:
        countries_list = ['UK', 'USA', 'Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of", 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']
    else:
        countries_list = ['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of", 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']
    return countries_list    


def create_df_countries(df, col):
    '''
    Returns a dataframe with number of times each country is mentioned in article. 

            Parameters:
                    df (DataFrame): a dataframe with at least one column of type string
                    col (str): name of a column in df

            Returns:
                    cited_countries (DataFrame)
    '''
    countries_list = countries(with_abbreviations=True)
    # Convert country names to lowercase to use it in the lower case news dataframe
    countries_list_lower = [country.lower() for country in countries_list]
    # Create a dictionary to revert country names back to correct form
    dic_lower_upper = {countries_list_lower[i]: countries_list[i] for i in range(len(countries_list_lower))}
    # Get ISO3 code for each country in list, add code for UK abreviation
    code_list = coco.convert(names=countries_list, to='ISO3')
    code_list[0] = 'GBR'
    dic_code_country = {countries_list[i]: code_list[i] for i in range(len(countries_list))}
    text = create_text(df, col)
    word_count = [(dic_lower_upper[word], text.count(word)) for word in countries_list_lower]    
    word_count = sorted(word_count, key=lambda i: i[1], reverse=True)
    x, y = zip(*word_count)        
    # Dataframe with countries and number of times they are mentioned in texts
    cited_countries = pd.DataFrame(word_count, columns =['Country', 'Number of times'])
    # Add column with country codes
    cited_countries['code'] = cited_countries['Country'].map(dic_code_country)
    # Consolidate rows: UK + United Kingdom, USA + United States
    united_kingdom = cited_countries.loc[cited_countries.Country=='United Kingdom']['Number of times'].item()
    uk = cited_countries.loc[cited_countries.Country=='UK']['Number of times'].item()
    cited_countries.loc[cited_countries.Country=='United Kingdom', 'Number of times']= united_kingdom + uk
    united_states = cited_countries.loc[cited_countries.Country=='United States']['Number of times'].item()
    usa = cited_countries.loc[cited_countries.Country=='USA']['Number of times'].item()
    cited_countries.loc[cited_countries.Country=='United States', 'Number of times']= united_states + usa
    cited_countries = cited_countries[cited_countries.Country.isin(['UK', 'USA'])==False]
    # Sort dataframe by number of times countries are cited
    cited_countries = cited_countries.sort_values(by=['Number of times'], ascending=False)
    return cited_countries


def create_map(df, projection_type):
    '''
    Returns a Plotly choropleth map showing how often countries are cited in articles.

            Parameters:
                    df (DataFrame): a dataframe with at least one column of type string
                    projection_type (str): type of projection as described in [Plotly's documentation](https://plotly.com/python/map-configuration/#map-projections)

            Returns:
                    cited_countries (DataFrame)
    '''
    fig = go.Figure(data=go.Choropleth(
        locations = df['code'],
        z = df['Number of times'],
        text = df['Country'],
        colorscale = 'GnBu',
        autocolorscale=False,
        reversescale=False,
        hoverinfo=["z"],
        hovertext = df['Country'],
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title = 'Number of<br>mentions',
    ))
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        geo=dict(
            showcoastlines=False,
            projection_type=projection_type,
            bgcolor= 'rgba(0,0,0,0)',
            oceancolor = 'rgba(220,220,220,0.1)',
            showframe = False,
            showocean = True   
        )
    )
    return fig

def load_data(file_path):
    '''
    Returns dataframe with raw data and a dataframe with lower case.

            Parameters:
                    file_path (str): path to raw data

            Returns:
                    df (DataFrame): raw data dataframe
                    df_lower (DataFrame): lower-case dataframe
    '''
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'], format="%m/%d/%Y")
    df_lower = df.apply(lambda x: x.astype(str).str.lower())
    df_lower['Date'] = pd.to_datetime(df_lower['Date'], format="%Y/%m/%d")
    return df, df_lower


def create_df_keywords(keywords_input, df_lower):
    '''
    Returns a dataframe with only rows that contain at least one of the keywords entered by user.

            Parameters:
                    keywords_input (list): list of keywords entered by user
                    df_lower (DataFrame): lower-case dataframe

            Returns:
                    input_df (DataFrame)
    '''
    keywords_input = keywords_input.lower()
    keywords_list = keywords_input.split(",")
    input_df = df_lower[df_lower.Text.str.contains('|'.join(keywords_list))==True]
    return input_df


def dates_article(df):
    '''
    Returns a dictionary with relevant dates related to the articles.
    
    Dictionary contains: date_max (last date of publication of an article containing at least one keyword), max_time_between_articles (maximal amount of time between articles), popular_month_year (month and year with most articles) and popular_year (most popular year).

            Parameters:
                    df (DataFrame): dataframe containing articles

            Returns:
                    dictionary
    '''
    df.reset_index(inplace=True, drop=True)
    def date_max(df):
        date_max = df.Date.max().strftime("%A, %d-%B-%Y")
        return {'date_max':date_max}

    def max_time_between_articles(df):    
        df['time_between'] = df["Date"].diff()
        max_time_between = df.time_between.max()
        index_max = df[df['time_between']==max_time_between].index.tolist()
        return {'max_time_between': f"{max_time_between.days} days", 
                'date_of_publication':df.loc[[index_max[0]]]['Date'].item().strftime("%A, %d-%B-%Y"), 
                'date_previous_publication':df.loc[[index_max[0]-1]]['Date'].item().strftime("%A, %d-%B-%Y")}
    
    def popular_month_year(df):
        month_year_row = df.groupby([pd.to_datetime(df['Date']).dt.year,
                           pd.to_datetime(df['Date']).dt.month]).Link.nunique().to_frame()
        max_month_year = month_year_row[month_year_row.Link==month_year_row.Link.max()].index.to_list()
        return {'month_year': f"{calendar.month_name[max_month_year[0][1]]} {max_month_year[0][0]}"}
    
    def popular_year(df):
        year = df.groupby(pd.to_datetime(df['Date']).dt.year).Link.nunique().to_frame()
        return {'year': year[year.Link==year.Link.max()].index.item()}
    
    df = df.sort_values(by=['Date'], ascending=True)
    df = df.reset_index(drop=True)
    return date_max(df) | max_time_between_articles(df) | popular_month_year(df) | popular_year(df)
    
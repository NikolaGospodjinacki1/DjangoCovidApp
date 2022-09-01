
import json

import numpy as np
import pandas as pd
import requests
from django.http import HttpResponse
from django.shortcuts import render


def get_api_data(api_url = "https://api.covid19api.com/summary"):
    api_data = requests.get(api_url).json()
    used_data = api_data['Countries']
    dataframe = pd.DataFrame.from_dict(used_data, orient="columns")
    
    return dataframe

def pandas_filter_data(dataframe = get_api_data()):
    dataframe = dataframe.iloc[:,np.r_[1:3,4:11].copy()]
    dataframe.set_index("Country", inplace=True)  
    numeric_columns = [
                       'NewConfirmed',
                       'TotalConfirmed',
                       'NewDeaths',
                       'TotalDeaths',
                       'NewRecovered',
                       'TotalRecovered'
    ]
    dataframe.loc['Total']= dataframe.sum(numeric_only=True, axis=0)
    dataframe[numeric_columns] = dataframe[numeric_columns].astype(int)
    return dataframe

def render_data_view(request, dataframe=pandas_filter_data()):
    query_dict = request.GET
    query = query_dict.get("query")
    if query:
        dataframe = dataframe.query('Country.str.contains(@query)', engine={'python'})
    json_frame = dataframe.reset_index().to_json(
                                                 orient="records",
                                                 date_unit='s',
                                                 
                                                 )
    final_data = json.loads(json_frame) 
    return render(request, "covid_api_data.html", {'data': final_data })

def export_data_to_csv(request, dataframe=pandas_filter_data()):
    query_dict = request.GET
    query = query_dict.get("query")
    if query:
        dataframe = dataframe.query('Country.str.contains(@query)', engine={'python'})
    response = HttpResponse(
                            content_type='text/csv',
                            headers={'Content-Disposition': f'attachment; filename="covid_data_{query}.csv"'}
                            )
    dataframe.to_csv(path_or_buf=response, sep=',', index=True)
    return response

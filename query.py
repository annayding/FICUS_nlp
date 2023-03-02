import os
import dimcli
from dimcli.utils import *
import pandas as pd
import numpy as np

# Dimensions Login & DSL
dimcli.login(key="02CB1C5A52B5430AA173E8D88F59A986",  
                 endpoint="https://app.dimensions.ai/api/dsl/v2")
dsl = dimcli.Dsl()

def runQuery_title_year(df_in):

    df_titles_years = df_in[["Title", "Date"]]

    df_out = pd.DataFrame()
    query_results = []
    yes_result = []
    no_result = []
    no_date = []
    bad_format = []

    i = 0
    imax = len(df_titles_years)

    for index, element in df_titles_years.iterrows():

        i+=1
        if i == imax:
            break

        # Only accept references with proper format
        try:
            # separate dateless refs
            if element[1] == ' ':
                no_date.append([element[0],element[1]])
                continue
            else:
                # remove colons/brackets    
                title = str(element[0]).replace(":","").replace("[","").replace("]","")
                # format YYYY
                year = int(element[1][-5:-1])
                # remove unreasonable years  
                if year < 1800 or year > 2023:
                    raise Exception
        except Exception:
            bad_format.append([element[0],element[1]])
            continue

        print("\nTitle: " + title + ", Year: " + str(year))

        # DSL query by title, year
        query = f"""
                search publications in title_only 
                    for "{dsl_escape(title)}" 
                    where year = {year}
                return publications limit 1
                """
        df = dsl.query(query).as_dataframe()

        # Separate into succesful/unsuccesful references
        if df is None:
            no_result.append([title,year])
        elif len(df) == 0:
            no_result.append([title,year])
        else:
            yes_result.append([title,year])
            query_results.append(df)


    df_out = pd.concat(query_results).\
                drop_duplicates(subset='id')
    
    print('Yes: ' + str(len(yes_result)))
    print('No: ' + str(len(no_result)))
    print('Dateless: ' + str(len(no_date)))
    print('Bad Format: ' + str(len(bad_format)))
    
    return df_out, yes_result, no_result, no_date, bad_format

    
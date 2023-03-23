import os
import dimcli
from dimcli.utils import *
import pandas as pd
import numpy as np 

# TODO: regex the dates in extract_year
# TODO: separate results into folders
# TODO: run the negative queries with partial string match

class InvalidQueryTypeException(Exception):
    "Raised when the query type is not 'exact' or 'fuzzy'"
    pass

def login():

    dimcli.login(key="02CB1C5A52B5430AA173E8D88F59A986",  
                 endpoint="https://app.dimensions.ai/api/dsl/v2")

    return dimcli.Dsl()

def format_title(title):

    bad_punctuation = [':', '[', ']', '"']
    title_str = str(title)

    for p in bad_punctuation:
        title_str = title_str.replace(p,"")

    return title_str

def extract_year(date):
    return int(date[-5:-1])

def query_exact_title_year(title, year):
    exact_title = '"' + '\\"' + title + '\\"' + '"'
    query = f"""
        search publications in title_only 
            for {exact_title} 
            where year = {year}
        return publications[id+title+year+journal] limit 1
        """
    return query

def query_fuzzy_title_year(title, year):
    query = f"""
        search publications in title_only 
            for "{dsl_escape(title)}" 
            where year = {year}
        return publications[id+title+year+journal] limit 1
        """
    return query

def query_fuzzy_title_year_author(title, year, author):
    query = f"""
        search publications in title_only 
            for "{dsl_escape(title)}" 
            where year = {year}
            where authors = {author}
        return publications[id+title+year+authors+journal] limit 1
        """
    return query

def run_query(df, q_type="exact"):

    dsl = login()
    df_titles_years = df[["Title", "Date"]]

    # TODO: turn into dataframes, use for output
    query_results = []
    yes_result = []
    no_result = []
    no_date = []
    bad_format = []
    results_df = pd.DataFrame()

    for index, [title, date] in df_titles_years.iterrows():

        # Force loop to end
        num_rows = len(df_titles_years)
        if index + 1 == num_rows:
            break

        # Only accept references with proper format
        try:
            # separate dateless refs
            if date == ' ':
                no_date.append([title,date])
                continue
            else:
                # remove colons/brackets    
                title = format_title(title)
                # format YYYY
                year = extract_year(date)
                # remove unreasonable years  
                if year < 1800 or year > 2023:
                    raise Exception
        except Exception:
            bad_format.append([title,date])
            continue

        print("\n" + str(index) + "/" + str(num_rows))
        print(title + " [" + str(year)  + "]") 

        # DSL query by title, year
        try: 
            if q_type == "exact":
                query = query_exact_title_year(title, year)
            elif q_type == "fuzzy":
                query = query_fuzzy_title(title, year)
            else:
                raise InvalidQueryTypeException

        except InvalidQueryTypeException:
            print("Invalid query type, retry with valid q_type string")
            break
        
        query_df = dsl.query(query).as_dataframe()

        # Separate into succesful/unsuccesful references
        if query_df is None:
            no_result.append([title,year]) # df.iloc[index]
        elif len(query_df) == 0:
            no_result.append([title,year])
        else:
            yes_result.append([title,year])
            query_results.append(query_df)


    results_df = pd.concat(query_results).\
                drop_duplicates(subset='id')
    
    print('Yes: ' + str(len(yes_result)))
    print('No: ' + str(len(no_result)))
    print('Dateless: ' + str(len(no_date)))
    print('Bad Format: ' + str(len(bad_format)))
    
    return results_df, yes_result, no_result, no_date, bad_format

def query_by_path(csv_path, q_type="exact"):
    return run_query(pd.read_csv(csv_path), q_type=q_type)
    
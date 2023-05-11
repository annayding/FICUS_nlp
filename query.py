import dimcli
import pandas as pd
import numpy as np 
import re


class InvalidQueryTypeException(Exception):
    "Raised when the query type is not 'exact' or 'fuzzy'"
    pass

def login(key_in="", endpoint_in="https://app.dimensions.ai/api/dsl/v2"):
    """ Inputs: key, endpoint 
        Outputs: Dimcli DSL query client
    """
    dimcli.login(key=key_in, endpoint=endpoint_in)
    return dimcli.Dsl()

def format_title(title):
    """ Input: title from df 
        Outputs: string title with colons, brackets and quotation marks removed
    """
    bad_punc = [':', '[', ']', '"']
    title_str = str(title)

    for p in bad_punc:
        title_str = title_str.replace(p,"")

    return title_str

# TODO: regex the dates in extract_year
def extract_year(date):
    """ Input: string date
        Output: string year
    """
    regex = "\d\d\d\d"
    return re.search(regex, date).group()

def query_exact_title_year(title, year):
    """ Input: String title, string year
        Output: Query string to query for an exact title and year match
    """
    exact_title = '"' + '\\"' + title + '\\"' + '"'
    query = f"""
        search publications in title_only 
            for {exact_title} 
            where year = {year}
        return publications[id+title+year+journal] limit 1
        """
    return query

def query_fuzzy_title_year(title, year):
    """ Input: String title, string year
        Output: Query string to query for a fuzzy title and year match
    """
    query = f"""
        search publications in title_only 
            for "{dsl_escape(title)}" 
            where year = {year}
        return publications[id+title+year+journal] limit 1
        """
    return query

def query_fuzzy_title_year_author(title, year, author):
    """ Input: String title, string year
        Output: Query string to query for a fuzzy title, year, and author match
    """
    query = f"""
        search publications in title_only 
            for "{dsl_escape(title)}" 
            where year = {year}
            where authors = {author}
        return publications[id+title+year+authors+journal] limit 1
        """
    return query

def run_query(df, q_type="exact"):
    """ Input: dataframe of references
        Param: query type, "exact" or "fuzzy"
        Outputs:
            positive_results - dataframe of positive query results
            negative_results - dataframe of references that returned a null query result
            dateless - dataframe of references that have no date
            bad_format - dataframe of references with bad title or date formatting
    """
    dsl = login()

    query_result_array = []
    positive_results = pd.DataFrame()
    negative_results = pd.DataFrame()
    dateless = pd.DataFrame()
    bad_format = pd.DataFrame()

    df_titles_years = df[["Title", "Date"]]

    for index, [title, date] in df_titles_years.iterrows():

        # Force loop to end
        num_rows = len(df_titles_years)
        if index + 1 == num_rows:
            break

        # Only accept references with proper format
        try:
            # separate dateless refs
            if date == ' ':
                dateless = pd.concat([dateless, df.iloc[index].to_frame().T], axis=0)
                continue
            else:
                # remove colons/brackets    
                title = format_title(title)
                # format YYYY
                year = extract_year(date)
                # remove unreasonable years  
                if int(year) < 1800 or int(year) > 2023:
                    raise Exception

        except Exception:
            bad_format = pd.concat([bad_format, df.iloc[index].to_frame().T], axis=0)
            continue

        print("\n" + str(index) + "/" + str(num_rows))
        print(title + " [" + str(year)  + "]") 

        # DSL query by title, year
        try: 
            if q_type == "exact":
                query = query_exact_title_year(title, year)
            elif q_type == "fuzzy":
                query = query_fuzzy_title_year(title, year)
            else:
                raise InvalidQueryTypeException
        except InvalidQueryTypeException:
            print("Invalid query type, retry with valid q_type string")
            break
        
        query_df = dsl.query(query).as_dataframe()

        # Separate into succesful/unsuccesful references
        if query_df is None:
            negative_results = pd.concat([negative_results, df.iloc[index].to_frame().T], axis=0)
        elif len(query_df) == 0:
            negative_results = pd.concat([negative_results, df.iloc[index].to_frame().T], axis=0)
        else:
            query_result_array.append(query_df)

    if len(query_result_array) != 0:
        positive_results = pd.concat(query_result_array).drop_duplicates(subset='id')

    print('Yes: ' + str(len(positive_results)))
    print('No: ' + str(len(negative_results)))
    print('Dateless: ' + str(len(dateless)))
    print('Bad Format: ' + str(len(bad_format)))
    
    return positive_results, negative_results, dateless, bad_format

def convert_results_to_csv(query_results, report):
    '''Converts query results into csv files and separates into respective folders
        Input: query_results, the dataframes returned by the run_query function
        Input: report, the queried report formatted as a string 'report_title.csv'
    '''
    positive_results, negative_results, dateless, bad_format = query_results

    if len(positive_results) > 0:
        positive_results.to_csv('dsl_query_results/positive_results/positive_' + report)
    if len(negative_results) > 0:
        negative_results.to_csv('dsl_query_results/negative_results/negative_' + report)
    if len(dateless) > 0:
        dateless.to_csv('dsl_query_results/dateless/dateless_' + report)
    if len(bad_format) > 0:
        bad_format.to_csv('dsl_query_results/bad_format/bad_format_' + report)
    return  

def query_by_path(csv_path, q_type="exact"):
    """ Input: string of path to csv
        Param: query type, "exact" or "fuzzy"
        Output: run_query function using dataframe of references from path
    """
    return run_query(pd.read_csv(csv_path), q_type=q_type)

def query_ssh(report, q_type="exact"):
    ''' Input: the queried report formatted as a string 'report_title.csv'
        Param: query type "exact" or "fuzzy"
    '''
    q = query_by_path('csv_refs_v2/' + report, q_type=q_type)
    convert_results_to_csv(q, report)
    return

    

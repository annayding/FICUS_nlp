import pandas as pd
import numpy as np
import xml.etree.cElementTree as et
import os

dir = os.path.dirname(os.path.realpath(__file__))
dir = dir + "/xml_refs/"
title_list = [file for file in os.listdir(dir)]

for xml in title_list:

    tree=et.parse(dir + "/" + xml)
    root=tree.getroot()

    Author = []
    Date = []
    Title = []
    Journal = []
    Volume = []
    Pages = []

    for author in root.iter('author'):
        Author.append(author.text)

    for date in root.iter('date'):
        Date.append(date.text)

    for title in root.iter('title'):
        Title.append(title.text)

    for journal in root.iter('journal'):
        Journal.append(journal.text)

    for volume in root.iter('volume'):
        Volume.append(volume.text)

    for pages in root.iter('pages'):
        Pages.append(pages.text)

    refs_df = pd.DataFrame(
                        list(zip(Title, Author, Date, Journal, Volume, Pages)), 
                        columns=['Title', 'Author', 'Date', 'Journal', 'Volume', 'Pages'])

    refs_df.to_csv("DimCLI/csv_refs/" + xml[:-4] + ".csv")
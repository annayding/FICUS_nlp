import pandas as pd
import numpy as np
import xml.etree.cElementTree as et
import os

refs_folder = '/xml_refs/'
outdir = './csv_refs_v2/'

if not os.path.exists(outdir):
    os.mkdir(outdir)

dir = os.path.dirname(os.path.realpath(__file__)) + refs_folder

for xml in os.listdir(dir):

    tree = et.parse(dir + '/' + xml)
    root = tree.getroot()

    Author = []
    Date = []
    Title = []
    Journal = []
    Volume = []
    Pages = []

    # TODO: fix missing first reference?
    for sequence in root.findall('sequence'):
        
        author = sequence.find('author')
        if author is not None:
            Author.append(author.text)
        else:
            Author.append(' ')

        date = sequence.find('date')
        if date is not None:
            Date.append(date.text)
        else:
            Date.append(' ')

        title = sequence.find('title')
        if title is not None:
            Title.append(title.text)
        else:
            Title.append('')

        journal = sequence.find('journal')
        if journal is not None:
            Journal.append(journal.text)
        else:
            Journal.append('')

        volume = sequence.find('volume')
        if volume is not None:
            Volume.append(volume.text)
        else:
            Volume.append('')

        pages = sequence.find('pages')
        if pages is not None:
            Pages.append(pages.text)
        else:
            Pages.append('')

    refs_df = pd.DataFrame(
                        list(zip(Title, Author, Date, Journal, Volume, Pages)), 
                        columns=['Title', 'Author', 'Date', 'Journal', 'Volume', 'Pages'])

    outname = xml[:-4] + '.csv'   
    fullname = os.path.join(outdir, outname)  
    refs_df.to_csv(fullname)
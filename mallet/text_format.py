import os
import ftfy
import nltk

# set your directory
dir = '/Users/jbakken/Desktop/HMC/2022_Fall/Research/Mallet/epa_1996/'

# take in a text file (e.g. OCR EPA report)
originalTxt = dir + '1996_v1_2.txt'

# create new files (some temporary)
filteredTxt = dir + 'filtered_text_tempFile.txt'
docsTxt = dir + 'split_documents_tempFile.txt'
tsv = dir + 'segmented_documents_with_refs.txt'

# clean the text (dependent on the input file)
# latin-1 avoids encoding probs, then ftfy converts back to utf-8
with open(filteredTxt, 'a') as f:
    for line in open(originalTxt, encoding = "latin-1"):
        try:
            if len(line) < 150:
                continue
            if line.upper() == line:
                continue
            elif '....' in line: 
                continue 
            f.write(ftfy.fix_text(line))
        except:
            continue

# read all tokens to list
allTokens = []
unwantedPunctuation = ["''", "``", '"', "'", "(", ")", "[", "]", ";", ",", ":"]
for line in open(filteredTxt, 'r'):
    for sentence in nltk.sent_tokenize(line):
        for token in nltk.word_tokenize(sentence):
            if token not in unwantedPunctuation:
                allTokens += [token]
        # newline to signify the end of a sentence
        if allTokens[-1]  == ".":
            allTokens += ['\n']

# group into 500+ word documents separated by newlines 
i = 1
line_breaker = 500
with open(docsTxt, 'a') as f:
    for token in allTokens:
        if(i >= line_breaker and token == "\n"):
            f.write(token)
            i = 0
        elif token != "\n":
            f.write(token + " ")
        i += 1

# place documents in an array 
documents = [line.rstrip('\n') for line in open(docsTxt, 'r')]

# format documents as tsv
with open(tsv, 'w') as f:
    i = 0
    for document in documents:
        label = str(i)
        identifier = 'Doc' + label
        f.write(identifier + '\t' + label + '\t' + document + '\n')
        i += 1

# remove intermediate files
os.remove(filteredTxt)
os.remove(docsTxt)



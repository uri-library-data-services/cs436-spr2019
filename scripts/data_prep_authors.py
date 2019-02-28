# Extract author data from "authors" file
#
# Inputs:
# ../data_output/ai-authors.tsv
#
# Outputs:
# ../data_output/authors.csv

import csv
import pandas as pd
import json
doc = "../data_output/ai-authors.tsv"
df = pd.read_csv(doc, sep='\t', header=None)

# add column names
df.columns = ['type', 'path', 'revisions', 'timestamp', 'details']

​# get 'author_id' from 'path'
df['author_id'] = df.path.str[9:]

​# create a list of lists containing only the id and json data fields
authors = df[['author_id', 'details']].values.tolist()
author_ids = ['author_id', 'author_name']  # initialize a list to hold extracted data

# iterate through the list and extract author names from the json data
for author in authors:
    details = json.loads(author[1])

    # append author_id and name to list
    author_ids.append([author[0], details["name"]])

# write author_ids list to a csv file
with open("../data_output/authors.csv", 'w', encoding='utf-8') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(author_ids)

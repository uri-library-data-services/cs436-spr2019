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


#
# read authors
#

doc = "../data_output/ai-authors.tsv"
df = pd.read_csv(doc, sep='\t', header=None)

# add column names
df.columns = ['type', 'path', 'revisions', 'timestamp', 'details']

# get 'author_id' from 'path'
df['author_id'] = df.path.str[9:]

# create a list of lists containing only the id and json data fields
authors = df[['author_id', 'details']].values.tolist()
author_ids = [['id', 'name']]  # initialize a list to hold extracted data

# iterate through the list and extract author names from the json data
for author in authors:
    details = json.loads(author[1])

    # append author_id and name to list
    author_ids.append([author[0], details["name"]])

# write author_ids list to a csv file
with open("../data_output/authors.csv", 'w', encoding='utf-8') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(author_ids)


#
# editions
#

# Inputs:
# ../data_output/ai-editions.tsv
#
# Outputs:
# ../data_output/editions_works.csv
# ../data_output/editions.csv


doc = "../data_output/ai-editions.tsv"
df = pd.read_csv(doc, sep='\t', header=None)

# add column names
df.columns = ['type', 'path', 'revisions', 'timestamp', 'details']

# get 'work_id' from 'path'
df['edition_id'] = df.path.str[7:]

# create a list of lists containing only the id and json data
editions_master = df[['edition_id', 'details']].values.tolist()
#
# PASS 1
#

edition_publisher = [["edition_id", "publisher_id"]]
publisher_place = [["pub_id", "place_id"]]
publisher_ids = {"NULL": "0"} # pub_name => pub_id
place_ids = {"NULL": "0"} # place_name => place_id
pub_id = 1
place_id = 1
for edition in editions_master:
    details = json.loads(edition[1])

    if 'publishers' in details.keys():
        publisher = details['publishers'][0]

        # create a unique id for publisher
        if publisher not in publisher_ids.keys():
            publisher_ids[publisher] = str(pub_id)
            pub_id += 1

        if 'publish_places' in details.keys():
            pub_place = details['publish_places'][0]
        else:
            pub_place = "NULL"
        # create a unique id for publisher place
        if pub_place not in place_ids.keys():
            place_ids[pub_place] = str(place_id)
            place_id += 1

        if 'publish_date' in details.keys():
            pub_date = details['publish_date']
            m = re.findall('\d\d\d\d', pub_date)
            if len(m):
                pubyear = m[0]
            else:
                pubyear = ""
        else:
            pubyear = ""


#
# PASS 2
#
edition_work = ["editionid", "workid"] # edition_id, work_id pairs
edition_tbl = [["id", "title", "numpages", "ISBN10", "ISBN13", "physfmt", "pubdate"]]
# also grab pubplace and pubyear in lists to use later
for edition in editions_master:
    details = json.loads(edition[1])
    # get work_ids -- lookup table
    edition_work.append([edition[0], details['works'][0]['key'][7:]])
    # get number of pages
    if 'number_of_pages' in details.keys():
        number_of_pages = details["number_of_pages"]
    else:
        number_of_pages = "NULL"
    # get isbn10 (Note: occasionally there are multiple ISBN's so to simplify we 
    # only select the first one)
    if 'isbn_10' in details.keys():
        isbn_10 = details["isbn_10"][0]
    else:
        isbn_10 = "NULL"
    # get isbn13 (Note: occasionally there are multiple ISBN's so to simplify we 
    # only select the first one)
    if 'isbn_13' in details.keys():
        isbn_13 = details["isbn_13"][0]
    else:
        isbn_13 = "NULL"
    # get title
    if 'title' in details.keys():
        title = details["title"]
    else:
        title = "NULL"
    # get format
    if 'physical_format' in details.keys():
        physical_format = details["physical_format"]
    else:
        physical_format = "NULL"
    # get publication date
    if 'publish_date' in details.keys():
        pub_date = details['publish_date']
    else:
        pub_date = "NULL"
    # get publication place
    if 'publish_date' in details.keys():
        pub_date = details['publish_date']
    else:
        pub_date = "NULL"

    edition_tbl.append([edition[0], number_of_pages, isbn_10, isbn_13, title, physical_format, pub_date])

with open("../data_output/edition_work.csv", 'w', encoding='utf-8', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(edition_work)

with open("../data_output/editions.csv", 'w', encoding='utf-8', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(edition_tbl)

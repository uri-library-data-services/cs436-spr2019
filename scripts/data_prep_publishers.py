# Extract publisher data from the "editions" myfile
#
# Inputs:
# ../data_output/ai-editions.tsv

# Outputs:
# ../data_output/edition_publisher.csv
# ../data_output/publisher_place.csv
# ../data_output/publishers.csv
# ../data_output/places.csv

import csv
import pandas as pd
import json
doc = "../data_output/ai-editions.tsv"
df = pd.read_csv(doc, sep='\t', header=None)

# add column names
df.columns = ['type', 'path', 'revisions', 'timestamp', 'details']

# get 'work_id' from 'path'
df['edition_id'] = df.path.str[7:]

# create a list of lists containing only the id and json data
editions_master = df[['edition_id', 'details']].values.tolist()
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

with open("../data_output/edition_publisher.csv", 'w', encoding='utf-8', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(edition_publisher)
with open("../data_output/publisher_place.csv", 'w', encoding='utf-8', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(publisher_place)

# publisher_ids and place_ids are dicts so they need to be handled differently
with open("../data_output/publishers.csv", 'w', encoding='utf-8', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(['pub_name', 'pub_id'])
    for key in publisher_ids.keys():
        wr.writerow([key, publisher_ids[key]])

with open("../data_output/places.csv", 'w', encoding='utf-8', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(['place_name', 'place_id'])
    for key in place_ids.keys():
        wr.writerow([key, place_ids[key]])

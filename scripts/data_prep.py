import re
import csv
import pandas as pd
import json


#
# Extract author data from "authors" file
#
# Inputs:
# ../data_output/ai-authors.tsv
#
# Outputs:
# ../data_output/authors.csv
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
# ../data_output/edition_publisher.csv
# ../data_output/publishers.csv
# ../data_output/places.csv

#
# Save:
# editionpub = {editionid:{publisherid:value,pubyear:value,pubplace:value}}
doc = "../data_output/ai-editions.tsv"
df = pd.read_csv(doc, sep='\t', header=None)

# add column names
df.columns = ['type', 'path', 'revisions', 'timestamp', 'details']

# get 'work_id' from 'path'
df['edition_id'] = df.path.str[7:]

edition_work = [["editionid", "workid"]] # edition_id, work_id pairs
edition_tbl = [["id", "title", "numpages", "ISBN10", "ISBN13", "physfmt", "pubdate"]]
editions_master = df[['edition_id', 'details']].values.tolist()
edition_publisher = [["editionid", "publisherid", "pubyear","pubplace"]]
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
        edition_publisher.append([edition[0],
                          publisher_ids[publisher],
                          pubyear,
                          place_ids[pub_place]]) 

    edition_work.append([edition[0], details['works'][0]['key'][7:]])
    # get number of pages
    if 'number_of_pages' in details.keys():
        number_of_pages = details["number_of_pages"]
    else:
        number_of_pages = "NULL"
    # get isbn10 
    if 'isbn_10' in details.keys():
        isbn_10 = details["isbn_10"][0]
    else:
        isbn_10 = "NULL"
    # get isbn13 
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
    if 'publish_date' in details.keys():
        pub_date = details['publish_date']
    else:
        pub_date = "NULL"
    edition_tbl.append([edition[0], title, number_of_pages, isbn_10, isbn_13, physical_format, pub_date])

with open("../data_output/edition_publisher.csv", 'w', encoding='utf-8', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(edition_publisher)

with open("../data_output/publishers.csv", 'w', encoding='utf-8', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(['id', 'name'])
    for key in publisher_ids.keys():
        wr.writerow([publisher_ids[key], key])
with open("../data_output/places.csv", 'w', encoding='utf-8', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(['id', 'name'])
    for key in place_ids.keys():
        wr.writerow([place_ids[key], key])
with open("../data_output/edition_work.csv", 'w', encoding='utf-8', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(edition_work)

with open("../data_output/editions.csv", 'w', encoding='utf-8', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(edition_tbl)
#quit()


# Process 'works' data
# Inputs:
# ../data_output/artificial_intelligence_works.txt

# Outputs:
# ../data_output/works.csv
# ../data_output/author_works.csv
# ../data_output/works_subject.csv
# ../data_output/subjects.csv

### Grab works data
doc = "../data_output/artificial_intelligence_works.txt"
df = pd.read_csv(doc, sep='\t', header=None)

# add column names
df.columns = ['type', 'path', 'revisions', 'timestamp', 'details']

# get 'work_id' from 'path'
df['work_id'] = df.path.str[7:]

# create a list containing only the id and json data
works = df[['work_id', 'details']].values.tolist()

# initialize some lists to hold the data that will get saved in csv files
titles = [["id","title"]] # work_id and title
work_authors = [["workid","authorid"]] # work_id and author_id
subjects = [] # temporary storage for work_id and subject
subject_tbl = [["id","subject"]] # subject_id
work_subject = [["workid","subjectid"]] #work_id and subject_id

# Loop through 'works' and pull out the pieces of data we want in the database
for work in works:
    details = json.loads(work[1])

    # append title to list
    titles.append([work[0], details["title"]])

    # append authors to list - not all works have authors!
    try:
        for a in details["authors"]:
            work_authors.append([work[0], a["author"]["key"][9:]])
    except:
        # print(json.dumps(details))
        continue

    # append subjects to list
    try:
        for s in details["subjects"]:
            subjects.append([work[0], s])
    except:
        # print(json.dumps(details))
        continue

# Create a set from the subjects list
unique_subjects = set()
for subject in subjects:
    unique_subjects.add(subject[1])

# Generate a subject id for each subject in the set.
n = 1
for u in sorted(unique_subjects):
    subject_tbl.append([str(n), u])
    n += 1

# Create a dictionary to allow subject lookups
subject_id = {}
for s in subject_tbl:
    subject_id[s[1]] = s[0]

# Create a list of lists containing pairs of subject id's and work id's

for s in subjects:
    work_subject.append([s[0], subject_id[s[1]]])

# Write "titles" to csv
with open("../data_output/works.csv", 'w', encoding='utf-8', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(titles)

# Write "work_authors" to csv
with open("../data_output/author_works.csv", 'w', encoding='utf-8', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(work_authors)

with open("../data_output/work_subjects.csv", 'w', encoding='utf-8', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(work_subject)

with open("../data_output/subjects.csv", 'w', encoding='utf-8', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(subject_tbl)


# Step 1: Process 'works' data
# Inputs:
# ../data_output/artificial_intelligence_works.txt

# Outputs:
# ../data_output/works.csv
# ../data_output/author_works.csv
# ../data_output/works_subject.csv
# ../data_output/subjects.csv

import csv
import json
import pandas as pd

doc = "../data_output/artificial_intelligence_works.txt"
df = pd.read_csv(doc, sep='\t', header=None)

# add column names
df.columns = ['type', 'path', 'revisions', 'timestamp', 'details']

# get 'work_id' from 'path'
df['work_id'] = df.path.str[7:]

# create a list containing only the id and json data
works = df[['work_id', 'details']].values.tolist()

# initialize some lists to hold the data that will get saved in csv files
titles = [["work_id","title"]] # work_id and title
work_authors = [["work_id","author_id"]] # work_id and author_id
subjects = [] # temporary storage for work_id and subject
subject_tbl = [["subject_id","subject"]] # subject_id
work_subject = [["work_id","subject_id"]] #work_id and subject_id
edition_publisher = [["edition_id","publisher_id"]] #edition_id and publisher_id

# Loop through 'works' and pull out the pieces of data we want in the database
for work in works:
    details = json.loads(work[1])

    # append title to list
    titles.append([work[0], details["title"]])

    # append authors to list - not all works have authors!
    try:
        for a in details["authors"]:
            # work_authors.append([works[0], json.dumps(a["author"]["key"][9:])])
            # author_id = json.dumps(a["author"]["key"][9:])
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

# Extract edition data from 'editions' file
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

edition_work = ["edition_id", "work_id"] # edition_id, work_id pairs
edition_tbl = [["edition_id","num_pages","isbn10","isbn13","physical_format",
                "title","pubdate"]]

for edition in editions_master:
    details = json.loads(edition[1])
    # get work_ids -- lookup table
    edition_work.append([edition[0], details['works'][0]['key'][7:]])
    # get number of pages
    if 'number_of_pages' in details.keys():
        number_of_pages = details["number_of_pages"]
    else:
        number_of_pages = "NULL"
    # get isbn10
    if 'isbn_10' in details.keys():
        isbn_10 = details["isbn_10"]
    else:
        isbn_10 = "NULL"
    # get isbn13
    if 'isbn_13' in details.keys():
        isbn_13 = details["isbn_13"]
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

    edition_tbl.append([edition[0], number_of_pages, isbn_10, isbn_13, title, physical_format, pub_date])

with open("../data_output/edition_work.csv", 'w', encoding='utf-8', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(edition_work)

with open("../data_output/editions.csv", 'w', encoding='utf-8', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(edition_tbl)

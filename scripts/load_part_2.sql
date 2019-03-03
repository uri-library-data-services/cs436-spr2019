-- load Author table from authors.csv
LOAD DATA LOCAL INFILE '../data_output/authors.csv' IGNORE
INTO TABLE Authors
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n';

-- load EditionWork
LOAD DATA LOCAL INFILE '../data_output/edition_work.csv' IGNORE
INTO TABLE EditionWork
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n'
(editionid, workid)
SET id = NULL;

-- load Editions
LOAD DATA LOCAL INFILE '../data_output/editions.csv' IGNORE
INTO TABLE Editions
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n';

-- load EditionPublish

-- load Publishers

-- load Works

-- load WorkAuthor
LOAD DATA LOCAL INFILE '../data_output/author_works.csv' IGNORE
INTO TABLE WorkAuthor
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n'
(workid, authorid)
SET id = NULL;

-- load Subjects

-- load WorkSubject

-- load Places

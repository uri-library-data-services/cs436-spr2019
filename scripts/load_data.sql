-- load Publishers
LOAD DATA LOCAL INFILE '../data_output/publishers.csv' IGNORE
INTO TABLE Publishers
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n';

-- load Editions
LOAD DATA LOCAL INFILE '../data_output/editions.csv' IGNORE
INTO TABLE Editions
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

-- load Author table from authors.csv
LOAD DATA LOCAL INFILE '../data_output/authors.csv' IGNORE
INTO TABLE Authors
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n';

-- load EditionPublish
LOAD DATA LOCAL INFILE '../data_output/edition_publisher.csv' IGNORE
INTO TABLE EditionPublish
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n'
(editionid, publisherid, pubyear, pubplace)
SET id = NULL;

-- load Places
LOAD DATA LOCAL INFILE '../data_output/places.csv' IGNORE
INTO TABLE Places
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n';

-- load Works
LOAD DATA LOCAL INFILE '../data_output/works.csv' IGNORE
INTO TABLE Works
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n';

-- load WorkAuthor
LOAD DATA LOCAL INFILE '../data_output/author_works.csv' IGNORE
INTO TABLE WorkAuthor
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n'
(workid, authorid)
SET id = NULL;

-- Subjects
LOAD DATA LOCAL INFILE '../data_output/subjects.csv' IGNORE
INTO TABLE Subjects
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n';

-- load WorkSubject
LOAD DATA LOCAL INFILE '../data_output/work_subjects.csv' IGNORE
INTO TABLE WorkSubject
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n'
(workid, subjectid)
SET id = NULL;

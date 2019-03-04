DROP TABLE IF EXISTS `Authors`;
CREATE TABLE `Authors` 
(
	`id` varchar(255) NOT NULL,
	`name` varchar(255),
        PRIMARY KEY(`id`)
);

DROP TABLE IF EXISTS `Publishers`;
CREATE TABLE `Publishers` 
(
	`publisherid` int NOT NULL,
	`name` varchar(255),
        PRIMARY KEY(`publisherid`)
);

DROP TABLE IF EXISTS `Editions`;
CREATE TABLE `Editions` 
(
	`id` varchar(255) NOT NULL,
	`title` varchar(255),
	`numpages` int,
	`ISBN10` varchar(255),
	`ISBN13` varchar(255),
	`physfmt` varchar(255),
	`pubdate` varchar(255),
        PRIMARY KEY(`id`)
);

DROP TABLE IF EXISTS `EditionWork`;
CREATE TABLE `EditionWork` 
(
	`id` int NOT NULL AUTO_INCREMENT,
	`editionid` varchar(255),
	`workid` varchar(255),
        PRIMARY KEY(`id`)
);

DROP TABLE IF EXISTS `EditionPublish`;
CREATE TABLE `EditionPublish` 
(
	`id` int NOT NULL AUTO_INCREMENT,
	`editionid` varchar(255),
	`publisherid` varchar(255),
	`pubyear` int,
	`pubplace` int,
        PRIMARY KEY(`id`)
);

DROP TABLE IF EXISTS `Places`;
CREATE TABLE `Places` 
(
	`id` int NOT NULL,
	`name` varchar(255),
        PRIMARY KEY(`id`)
);

DROP TABLE IF EXISTS `Works`;
CREATE TABLE `Works` 
(
	`id` varchar(255) NOT NULL,
	`title` varchar(255),
        PRIMARY KEY(`id`)
);

DROP TABLE IF EXISTS `WorkAuthor`;
CREATE TABLE `WorkAuthor` 
(
	`id` int NOT NULL AUTO_INCREMENT,
	`workid` varchar(255),
	`authorid` varchar(255),
        PRIMARY KEY(`id`)
);

DROP TABLE IF EXISTS `Subjects`;
CREATE TABLE `Subjects` 
(
	`id` int NOT NULL,
	`subject` varchar(255),
        PRIMARY KEY(`id`)
);

DROP TABLE IF EXISTS `WorkSubject`;
CREATE TABLE `WorkSubject` 
(
	`id` int NOT NULL AUTO_INCREMENT,
	`workid` varchar(255),
	`subjectid` varchar(255),
        PRIMARY KEY(`id`)
);


DROP TABLE
	WORK_EXPR,
	EDUCATIONAL_DETAILS,
	MESSAGE,
	CONNECTION_USR,
	USR
	CASCADE;

CREATE TABLE USR(
	userId varchar(50) UNIQUE NOT NULL, 
	password varchar(50) NOT NULL,
	email text NOT NULL,
	name char(50),
	dateOfBirth date,
	Primary Key(userId));

CREATE TABLE WORK_EXPR(
	userId varchar(50) NOT NULL, 
	company varchar(50) NOT NULL, 
	role char(50) NOT NULL,
	location char(50),
	startDate date,
	endDate date,
	PRIMARY KEY(userId,company,role,startDate),
	FOREIGN KEY(userId) REFERENCES USR);

CREATE TABLE EDUCATIONAL_DETAILS(
	userId char(50) NOT NULL, 
	institutionName char(50) NOT NULL, 
	major char(50) NOT NULL,
	degree char(50) NOT NULL,
	startdate date,
	enddate date,
	PRIMARY KEY(userId,major,degree),
	FOREIGN KEY(userId) REFERENCES USR);

CREATE TABLE MESSAGE(
	msgId integer UNIQUE NOT NULL, 
	senderId varchar(50) NOT NULL,
	receiverId varchar(50) NOT NULL,
	contents char(500) NOT NULL,
	sendTime timestamp,
	deleteStatus integer,
	status char(30) NOT NULL,
	PRIMARY KEY(msgId),
	FOREIGN KEY(senderId) REFERENCES USR(userId),
	FOREIGN KEY(receiverId) REFERENCES USR(userId));

CREATE TABLE CONNECTION_USR(
	userId varchar(50) NOT NULL, 
	connectionId varchar(50) NOT NULL, 
	status char(30) NOT NULL,
	PRIMARY KEY(userId,connectionId),
	FOREIGN KEY(userId) REFERENCES USR,
	FOREIGN KEY(connectionId) REFERENCES USR(userId));

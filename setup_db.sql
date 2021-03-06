CREATE TABLE `USERS` (
	`ID`	INTEGER NOT NULL CHECK(length ( ID ) > 0) PRIMARY KEY AUTOINCREMENT UNIQUE,
	`USERNAME`	TEXT NOT NULL CHECK(length ( USERNAME ) > 0) UNIQUE,
	`FIRSTNAME`	TEXT,
	`LASTNAME`	TEXT NOT NULL CHECK(length ( LASTNAME ) > 0),
	`MOBILE`	TEXT,
	`EMAIL`	TEXT,
	`EMPID`	TEXT,
	`ORGANIZATION`	TEXT NOT NULL CHECK(length ( ORGANIZATION ) > 0),
	`STATUS`	TEXT NOT NULL DEFAULT 'ACTIVE' CHECK(length ( STATUS ) > 0),
	`LAST_UPDATE`	NUMERIC NOT NULL DEFAULT 1,
	FOREIGN KEY(`ORGANIZATION`) REFERENCES `ORGS`(`ORG_ID`)
);


INSERT INTO USERS(USERNAME,FIRSTNAME,LASTNAME,MOBILE,EMAIL,EMPID,ORGANIZATION)
VALUES ('usr1', 'User', 'One', '0123456701', 'usr1@example.com', '0001', 'IT');

INSERT INTO USERS(USERNAME,FIRSTNAME,LASTNAME,MOBILE,EMAIL,EMPID,ORGANIZATION)
VALUES ('usr2', 'User', 'Two', '0123456702', 'usr2@example.com', '0002', 'FN');

INSERT INTO USERS(USERNAME,FIRSTNAME,LASTNAME,MOBILE,EMAIL,EMPID,ORGANIZATION)
VALUES ('usr3', 'User', 'Three', '0123456703', 'usr3@example.com', '0003', 'MK');

INSERT INTO USERS(USERNAME,FIRSTNAME,LASTNAME,MOBILE,EMAIL,EMPID,ORGANIZATION)
VALUES ('usr4', 'User', 'Four', '0123456704', 'usr4@example.com', '0004', 'SL');

INSERT INTO USERS(USERNAME,FIRSTNAME,LASTNAME,MOBILE,EMAIL,EMPID,ORGANIZATION)
VALUES ('usr5', 'User', 'Five', '0123456705', 'usr5@example.com', '0005', 'CC');

INSERT INTO USERS(USERNAME,FIRSTNAME,LASTNAME,MOBILE,EMAIL,EMPID,ORGANIZATION)
VALUES ('usr6', 'User', 'Six', '0123456706', 'usr6@example.com', '0006', 'CC');

INSERT INTO USERS(USERNAME,FIRSTNAME,LASTNAME,MOBILE,EMAIL,EMPID,ORGANIZATION)
VALUES ('usr7', 'User', 'Seven', '0123456707', 'usr7@example.com', '0007', 'CC');

CREATE TABLE `ORGS` (
	`ID`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`ORG_ID`	TEXT NOT NULL UNIQUE,
	`ORG_NAME`	TEXT NOT NULL UNIQUE
);

INSERT INTO ORGS(ORG_NAME, ORG_ID) VALUES ('Information Technology', 'IT');
INSERT INTO ORGS(ORG_NAME, ORG_ID) VALUES ('Finance', 'FN');
INSERT INTO ORGS(ORG_NAME, ORG_ID) VALUES ('Marketing', 'MK');
INSERT INTO ORGS(ORG_NAME, ORG_ID) VALUES ('Sales', 'SL');
INSERT INTO ORGS(ORG_NAME, ORG_ID) VALUES ('Customer Care', 'CC');

CREATE TABLE `ROLES` (
	`ROLE_ID`	TEXT,
	`ROLE_NAME`	TEXT NOT NULL,
	PRIMARY KEY(`ROLE_ID`)
);

INSERT INTO ROLES(ROLE_ID, ROLE_NAME) VALUES ('R1', 'Admin');
INSERT INTO ROLES(ROLE_ID, ROLE_NAME) VALUES ('R2', 'Developer');
INSERT INTO ROLES(ROLE_ID, ROLE_NAME) VALUES ('R3', 'Agent');
INSERT INTO ROLES(ROLE_ID, ROLE_NAME) VALUES ('R4', 'Manager');

CREATE TABLE `USER_ROLES` (
	`USER_ID`	INTEGER NOT NULL,
	`ROLE_ID`	TEXT NOT NULL,
	FOREIGN KEY(`ROLE_ID`) REFERENCES `ROLES`(`ROLE_ID`) ON DELETE CASCADE,
	FOREIGN KEY(`USER_ID`) REFERENCES `USERS`(`ID`) ON DELETE CASCADE
);

INSERT INTO USER_ROLES(USER_ID, ROLE_ID) VALUES (1, 'R1');
INSERT INTO USER_ROLES(USER_ID, ROLE_ID) VALUES (1, 'R2');
INSERT INTO USER_ROLES(USER_ID, ROLE_ID) VALUES (2, 'R1');
INSERT INTO USER_ROLES(USER_ID, ROLE_ID) VALUES (2, 'R2');
INSERT INTO USER_ROLES(USER_ID, ROLE_ID) VALUES (2, 'R3');
INSERT INTO USER_ROLES(USER_ID, ROLE_ID) VALUES (3, 'R4');
INSERT INTO USER_ROLES(USER_ID, ROLE_ID) VALUES (4, 'R4');
INSERT INTO USER_ROLES(USER_ID, ROLE_ID) VALUES (5, 'R3');
INSERT INTO USER_ROLES(USER_ID, ROLE_ID) VALUES (6, 'R1');
INSERT INTO USER_ROLES(USER_ID, ROLE_ID) VALUES (6, 'R4');
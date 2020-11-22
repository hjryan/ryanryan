PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Locales;
DROP TABLE IF EXISTS Walks;
DROP TABLE IF EXISTS Activities;
DROP TABLE IF EXISTS ActivitiesUsers;
DROP TABLE IF EXISTS ActivitiesLocales;
CREATE TABLE Locales(
localeID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
localeName VARCHAR(40) NOT NULL
);
INSERT INTO Locales(localeName) VALUES("Seattle");
INSERT INTO Locales(localeName) VALUES("Denver");
INSERT INTO Locales(localeName) VALUES("Mars");
INSERT INTO Locales(localeName) VALUES("the kitchen");
INSERT INTO Locales(localeName) VALUES("the grocery store");
CREATE TABLE Users(
userID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
firstName VARCHAR(40) NOT NULL,
lastName VARCHAR(40) NOT NULL,
localeID INTEGER,
FOREIGN KEY(localeID) REFERENCES Locales(localeID) ON DELETE SET NULL
);
INSERT INTO Users(firstName, lastName, localeID) VALUES("Hannah", "Ryan", "1");
INSERT INTO Users(firstName, lastName, localeID) VALUES("Ryan", "McKenzie", "2");
INSERT INTO Users(firstName, lastName, localeID) VALUES("Sam", "Ryan", "3");
CREATE TABLE Walks(
walkID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
walkName VARCHAR(40) NOT NULL,
destination INTEGER,
origin INTEGER,
userID INTEGER,
FOREIGN KEY(destination) REFERENCES Locales(localeID) ON DELETE SET NULL,
FOREIGN KEY(origin) REFERENCES Locales(localeID) ON DELETE SET NULL,
FOREIGN KEY(userID) REFERENCES Users(userID) ON DELETE SET NULL
);
INSERT INTO Walks(walkName, destination, origin, userID) VALUES("Very long walk", "2", "1", "1");
INSERT INTO Walks(walkName, destination, origin, userID) VALUES("Very long walk in reverse", "1", "2", "2");
CREATE TABLE Activities(
activityID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
activityName VARCHAR(40) NOT NULL
);
INSERT INTO Activities(activityName) VALUES("Call Arvind I guess");
INSERT INTO Activities(activityName) VALUES("Enjoy operating the flip");
CREATE TABLE ActivitiesUsers(
activityID INTEGER,
userID INTEGER,
FOREIGN KEY(activityID) REFERENCES Activities(activityID) ON DELETE SET NULL,
FOREIGN KEY(userID) REFERENCES Users(userID) ON DELETE SET NULL
);
INSERT INTO ActivitiesUsers(activityID, userID) VALUES (1,1);
INSERT INTO ActivitiesUsers(activityID, userID) VALUES (2,2);
CREATE TABLE ActivitiesLocales(
activityID INTEGER,
localeID INTEGER,
FOREIGN KEY(activityID) REFERENCES Activities(activityID) ON DELETE SET NULL,
FOREIGN KEY(localeID) REFERENCES Locales(localeID) ON DELETE SET NULL
);
INSERT INTO ActivitiesLocales(activityID, localeID) VALUES (1,1);
INSERT INTO ActivitiesLocales(activityID, localeID) VALUES (2,2);

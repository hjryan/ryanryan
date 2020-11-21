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
CREATE TABLE Users(
userID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
firstName VARCHAR(40) NOT NULL,
lastName VARCHAR(40) NOT NULL,
localeID INTEGER,
FOREIGN KEY(localeID) REFERENCES Locales(localeID) ON DELETE SET NULL
);
INSERT INTO Users(firstName, lastName, localeID) VALUES("Hannah", "Ryan", "1");
INSERT INTO Users(firstName, lastName, localeID) VALUES("Ryan", "McKenzie", "2");

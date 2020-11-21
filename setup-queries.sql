PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Locales;
DROP TABLE IF EXISTS Walks;
DROP TABLE IF EXISTS Activities;
DROP TABLE IF EXISTS ActivitiesUsers;
DROP TABLE IF EXISTS ActivitiesLocales;
CREATE TABLE Users(
userID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
firstName VARCHAR(40) NOT NULL,
lastName VARCHAR(40) NOT NULL,
localeID INTEGER
);
INSERT INTO Users(firstName, lastName) VALUES("Hannah", "Ryan");
INSERT INTO Users(firstName, lastName) VALUES("Ryan", "McKenzie");
SELECT * FROM Users;

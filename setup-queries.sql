DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Locales;
DROP TABLE IF EXISTS Walks;
DROP TABLE IF EXISTS Activities;
DROP TABLE IF EXISTS ActivitiesUsers;
DROP TABLE IF EXISTS ActivitiesLocales;
CREATE TABLE Users(
userID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
firstName VARCHAR(40) NOT NULL,
lastName VARCHAR(40) NOT NULL,
localeID INT
);
INSERT INTO Users(firstName, lastName) VALUES("Hannah", "Ryan");
INSERT INTO Users(firstName, lastName) VALUES("Ryan", "McKenzie");
CREATE TABLE Locales(
localeID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
localeName VARCHAR(40) NOT NULL
);
INSERT INTO Locales(localeName) VALUES("Seattle");
INSERT INTO Locales(localeName) VALUES("Denver");
ALTER TABLE Users
ADD FOREIGN KEY(localeID)
REFERENCES Locales(localeID)
ON DELETE SET NULL;
UPDATE Users
SET localeID = 1
WHERE userID = 1;
UPDATE Users
SET localeID = 2
WHERE userID = 2;
CREATE TABLE Walks(
walkID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
walkName VARCHAR(40) NOT NULL,
destination INT,
origin INT,
userID INT,
FOREIGN KEY(destination) REFERENCES Locales(localeID) ON DELETE SET NULL,
FOREIGN KEY(origin) REFERENCES Locales(localeID) ON DELETE SET NULL,
FOREIGN KEY(userID) REFERENCES Users(userID) ON DELETE SET NULL
);
INSERT INTO Walks(walkName, destination, origin, userID) VALUES("Very long walk", "2", "1", "1");
INSERT INTO Walks(walkName, destination, origin, userID) VALUES("Very long walk in reverse", "1", "2", "2");
CREATE TABLE Activities(
activityID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
activityName VARCHAR(40) NOT NULL
);
INSERT INTO Activities(activityName) VALUES("Call Arvind I guess");
INSERT INTO Activities(activityName) VALUES("Enjoy operating the flip");
CREATE TABLE ActivitiesUsers(
activityID INT,
userID INT,
FOREIGN KEY(activityID) REFERENCES Activities(activityID) ON DELETE SET NULL,
FOREIGN KEY(userID) REFERENCES Users(userID) ON DELETE SET NULL
);
INSERT INTO ActivitiesUsers(activityID, userID) VALUES (1,1);
INSERT INTO ActivitiesUsers(activityID, userID) VALUES (2,2);
CREATE TABLE ActivitiesLocales(
activityID INT,
localeID INT,
FOREIGN KEY(activityID) REFERENCES Activities(activityID) ON DELETE SET NULL,
FOREIGN KEY(localeID) REFERENCES Locales(localeID) ON DELETE SET NULL
);
INSERT INTO ActivitiesLocales(activityID, localeID) VALUES (1,1);
INSERT INTO ActivitiesLocales(activityID, localeID) VALUES (2,2);
-- Register
-- The registration page adds a new locale to the Locales table (localeName and an autoincremented localeID) if the locale does not yet exist.
INSERT INTO Locales(localeName) VALUES(:localeNameProvidedByUser);
-- If the locale does exist in the Users table, the user should not be permitted to register there. 
-- Then the new user is added to the Users table -- firstName, lastName, an autoincremented userID, and the localeID that was just added.
INSERT INTO Users(firstName, lastName, localeID) VALUES(:firstNameProvidedByUser, :firstNameProvidedByUser, (SELECT localeID FROM Locales WHERE localeName = :localeNameProvidedByUser);

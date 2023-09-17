DROP TABLE IF EXISTS counties;
CREATE TABLE counties
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    county TEXT NOT NULL,
    town TEXT NOT NULL
);
INSERT INTO counties(id, county, town)
VALUES 
       (1, "Kerry", "Listowel"),
       (2, "Dublin", "Swords"),
       (3, "Galway", "Claregalway"),
       (4, "Wexford", "Enniscorthy"),
       (5, "Antrim", "Belfast"),
       (6, "Carlow", "Clonmore"),
       (7, "Mayo", "Westport"),
       (8, "Sligo", "Enniscrone"),
       (9, "Louth", "Drogheda"),
       (10, "Laois", "Abbeyleix"),
       (11, "Waterford", "Ardmore"),
       (12, "Tipperary", "Cashel"),
       (13, "Roscommon", "Boyle"),
       (14, "Clare", "Lahinch"),
       (15, "Kildare", "Leixlip"),
       (16, "Kilkenny", "Callan"),
       (17, "Longford", "Granard"),
       (18, "Meath", "Trim"),
       (19, "Westmeath", "Mullingar"),
       (20, "Leitrim", "Carrick-on-Shannon"),
       (21, "Cavan", "Killashandra"),
       (22, "Donegal", "Letterkenny"),
       (23, "Monaghan", "Castleblayney"),
       (24, "Offaly", "Tullamore"),
       (25, "Cork", "Kinsale"),
       (26, "Limerick", "Abbeyfeale"),
       (27, "Cork", "Clonakilty");
       

       
       
       
       
       
       
       
       
       
       



DROP TABLE IF EXISTS users;
CREATE TABLE users
(
username TEXT PRIMARY KEY NOT NULL,
password TEXT NOT NULL,
point INTEGER 
);
DROP TABLE IF EXISTS comments;
CREATE TABLE comments
(
comment TEXT NOT NULL
);
INSERT INTO comments(comment)
VALUES
    ("So much fun"),
    ("love it"),
    ("Great game");

DROP TABLE IF EXISTS points;
CREATE TABLE points
(
username TEXT NOT NULL,
point INTEGER 
);
INSERT INTO points(username, point)
VALUES
    ("user7", 11);




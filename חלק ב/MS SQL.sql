CREATE TABLE persons (
    Person_Id INT PRIMARY KEY IDENTITY(1,1),
    Personal_Name NVARCHAR(50),
    Family_Name NVARCHAR(50),
    Gender NVARCHAR(10),
    Father_Id INT,
    Mother_Id INT,
    Spouse_Id INT,
    FOREIGN KEY (Father_Id) REFERENCES persons(Person_Id),
    FOREIGN KEY (Mother_Id) REFERENCES persons(Person_Id),
    FOREIGN KEY (Spouse_Id) REFERENCES persons(Person_Id)
);

INSERT INTO persons (Personal_Name, Family_Name, Gender)
VALUES (N'דני', N'כהן', N'זכר'),       -- 1
       (N'רותי', N'כהן', N'נקבה');     -- 2

INSERT INTO persons (Personal_Name, Family_Name, Gender, Father_Id, Mother_Id)
VALUES (N'אורן', N'כהן', N'זכר', 1, 2),    -- 3
       (N'יעל', N'כהן', N'נקבה', 1, 2);    -- 4
       
INSERT INTO persons (Personal_Name, Family_Name, Gender)
VALUES (N'אורי', N'לוי', N'זכר');         -- 5

INSERT INTO persons (Personal_Name, Family_Name, Gender, Father_Id, Mother_Id)
VALUES (N'נועה', N'לוי', N'נקבה', 5, 4),   -- 6
       (N'דן', N'לוי', N'זכר', 5, 4);  


CREATE TABLE relatives (
    Person_Id INT,
    Relative_Id INT,
    Connection_Type NVARCHAR(20)
);

-- קשרי אב
INSERT INTO relatives (Person_Id, Relative_Id, Connection_Type)
SELECT Person_Id, Father_Id, N'אב'
FROM persons
WHERE Father_Id IS NOT NULL;

-- קשרי אם
INSERT INTO relatives (Person_Id, Relative_Id, Connection_Type)
SELECT Person_Id, Mother_Id, N'אם'
FROM persons
WHERE Mother_Id IS NOT NULL;

-- קשרי ילדים (מהורה לילד)
INSERT INTO relatives (Person_Id, Relative_Id, Connection_Type)
SELECT Father_Id, Person_Id, N'בן'
FROM persons
WHERE Father_Id IS NOT NULL AND Gender = N'זכר';

INSERT INTO relatives (Person_Id, Relative_Id, Connection_Type)
SELECT Father_Id, Person_Id, N'בת'
FROM persons
WHERE Father_Id IS NOT NULL AND Gender = N'נקבה';

INSERT INTO relatives (Person_Id, Relative_Id, Connection_Type)
SELECT Mother_Id, Person_Id, N'בן'
FROM persons
WHERE Mother_Id IS NOT NULL AND Gender = N'זכר';

INSERT INTO relatives (Person_Id, Relative_Id, Connection_Type)
SELECT Mother_Id, Person_Id, N'בת'
FROM persons
WHERE Mother_Id IS NOT NULL AND Gender = N'נקבה';

-- קשר מבוסס על Spouse_Id
INSERT INTO relatives (Person_Id, Relative_Id, Connection_Type)
SELECT Person_Id,
       Spouse_Id,
       CASE WHEN Gender = N'זכר' THEN N'בת זוג' ELSE N'בן זוג' END
FROM persons
WHERE Spouse_Id IS NOT NULL;

UPDATE p2
SET p2.Spouse_Id = p1.Person_Id
FROM persons p1
JOIN persons p2 ON p1.Spouse_Id = p2.Person_Id
WHERE p2.Spouse_Id IS NULL;


-- קשרי אחים לפי אב
INSERT INTO relatives (Person_Id, Relative_Id, Connection_Type)
SELECT p1.Person_Id, p2.Person_Id,
       CASE WHEN p2.Gender = N'זכר' THEN N'אח' ELSE N'אחות' END
FROM persons p1
JOIN persons p2 ON p1.Father_Id = p2.Father_Id
WHERE p1.Person_Id <> p2.Person_Id AND p1.Father_Id IS NOT NULL;

-- קשרי אחים לפי אם
INSERT INTO relatives (Person_Id, Relative_Id, Connection_Type)
SELECT p1.Person_Id, p2.Person_Id,
       CASE WHEN p2.Gender = N'זכר' THEN N'אח' ELSE N'אחות' END
FROM persons p1
JOIN persons p2 ON p1.Mother_Id = p2.Mother_Id
WHERE p1.Person_Id <> p2.Person_Id AND p1.Mother_Id IS NOT NULL;


SELECT * FROM relatives;

SELECT * from persons;
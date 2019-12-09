SELECT 
	id, 
	CONCAT(firstname, ' ', lastname) as full_name, 
    YEAR(birthdate) as birth_year 
FROM 
	`employee`;

//==========================================================

INSERT INTO employee
	(`firstname`, `lastname`, `birthdate`)
    VALUES ('Noname', 'Nonameov', '2000-02-28 15-16-17');

//==========================================================

SELECT 
	*
FROM 
	`employee`
WHERE 
	MONTH(birthdate) < 06 AND HOUR(birthdate) > 13;

//==========================================================
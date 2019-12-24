-- Проверка на корректные даты при добавлении работника

BEGIN

IF NEW.birthday >= NEW.employ_date OR (NEW.unemploy_date IS NOT NULL AND NEW.employ_date >= NEW.unemploy_date) THEN
SIGNAL SQLSTATE '10001'
  SET MESSAGE_TEXT = 'Error! Incorrect date!';
END IF;

END
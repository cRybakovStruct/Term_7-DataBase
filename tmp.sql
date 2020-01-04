-- Проверка на корректные даты при добавлении работника
BEGIN IF NEW.birthday >= NEW.employ_date
OR (
  NEW.unemploy_date IS NOT NULL
  AND NEW.employ_date >= NEW.unemploy_date
) THEN SIGNAL SQLSTATE '10001'
SET
  MESSAGE_TEXT = 'Error! Incorrect date!';

END IF;

END -- Отображение сводной информации
SELECT
  fixations.worker,
  workers.surname,
  workers.name,
  fixations.shop
from
  fixations
  LEFT JOIN workers ON fixations.worker = workers.idworker;

BEGIN
SELECT
  repairs.idrepair,
  repairs.repair_name,
  repairs.is_planned,
  repairs.receipt_date,
  repairs.start_date,
  repairs.finish_date,
  repairs.responsible_id,
  workers.surname,
  workers.name,
  repairs.equipment_id,
  equipment.model,
  equipment.placement
FROM
  repairs
  LEFT JOIN workers ON repairs.responsible_id = workers.idworker
  LEFT JOIN equipment ON repairs.equipment_id = equipment.serial_number;

END
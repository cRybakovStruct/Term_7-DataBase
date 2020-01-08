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

END -- Фильтрация сложного запроса (можно ли как-то его сократить?).
BEGIN IF field_var = 'idrepair' THEN
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
  LEFT JOIN equipment ON repairs.equipment_id = equipment.serial_number
WHERE
  repairs.idrepair = CONVERT(value_var, INTEGER);

ELSEIF field_var = 'repair_name' THEN
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
  LEFT JOIN equipment ON repairs.equipment_id = equipment.serial_number
WHERE
  repairs.repair_name = CONVERT(value_var, VARCHAR(45));

ELSEIF field_var = 'is_planned' THEN
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
  LEFT JOIN equipment ON repairs.equipment_id = equipment.serial_number
WHERE
  repairs.is_planned = CONVERT(value_var, INTEGER);

ELSEIF field_var = 'receipt_date' THEN
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
  LEFT JOIN equipment ON repairs.equipment_id = equipment.serial_number
WHERE
  repairs.receipt_date = CONVERT(value_var, DATE);

ELSEIF field_var = 'start_date' THEN
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
  LEFT JOIN equipment ON repairs.equipment_id = equipment.serial_number
WHERE
  repairs.start_date = CONVERT(value_var, DATE);

ELSEIF field_var = 'finish_date' THEN
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
  LEFT JOIN equipment ON repairs.equipment_id = equipment.serial_number
WHERE
  repairs.finish_date = CONVERT(value_var, DATE);

ELSEIF field_var = 'responsible_id' THEN
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
  LEFT JOIN equipment ON repairs.equipment_id = equipment.serial_number
WHERE
  repairs.responsible_id = CONVERT(value_var, INTEGER);

ELSEIF field_var = 'surname' THEN
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
  LEFT JOIN equipment ON repairs.equipment_id = equipment.serial_number
WHERE
  workers.surname = CONVERT(value_var, VARCHAR(45));

ELSEIF field_var = 'name' THEN
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
  LEFT JOIN equipment ON repairs.equipment_id = equipment.serial_number
WHERE
  workers.name = CONVERT(value_var, VARCHAR(45));

ELSEIF field_var = 'equipment_id' THEN
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
  LEFT JOIN equipment ON repairs.equipment_id = equipment.serial_number
WHERE
  repairs.equipment_id = CONVERT(value_var, INTEGER);

ELSEIF field_var = 'model' THEN
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
  LEFT JOIN equipment ON repairs.equipment_id = equipment.serial_number
WHERE
  equipment.model = CONVERT(value_var, VARCHAR(45));

ELSEIF field_var = 'placement' THEN
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
  LEFT JOIN equipment ON repairs.equipment_id = equipment.serial_number
WHERE
  equipment.placement = CONVERT(value_var, VARCHAR(45));

END IF;

END
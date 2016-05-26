--check how many records exist on db:
SELECT SUM(TABLE_ROWS)
     FROM INFORMATION_SCHEMA.TABLES
     WHERE TABLE_SCHEMA = 'hoc_db';
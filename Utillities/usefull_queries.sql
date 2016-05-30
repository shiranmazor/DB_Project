--check how many records exist on db:
SELECT SUM(TABLE_ROWS)
     FROM INFORMATION_SCHEMA.TABLES
     WHERE TABLE_SCHEMA = 'hoc_db';

---create index on screen_name in users table
CREATE INDEX screen_name_index ON  users(screen_name) USING BTREE;
---create index on full_name in users table
CREATE INDEX full_name_index ON  users(full_name) USING BTREE;



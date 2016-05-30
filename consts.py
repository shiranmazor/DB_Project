DB_HOSTNAME = '127.0.0.1'
DB_USER = 'root'
DB_PASSWORD = 'tata2901'
DB_NAME = 'hoc_db'

#query format :INSERT INTO TABLE_NAME (f1,f2..) VALUES (%s, %s, %s, %s, %s)
INSERT_QUERY = 'INSERT INTO {0} ({1}) VALUES '
#query format :SELECT * TABLE_NAME WHERE id=id_val
SELECT_BY_ID = 'SELECT * FROM {0} WHERE id={1}'
#query format :SELECT * TABLE_NAME WHERE filed_name=filed_val
SELECT_BY_FIELD = 'SELECT * FROM {0} WHERE {1}={2}'
# UPDATE table_nameS ET column1=value, column2=value2,... WHERE some_column=some_value
UPDATE_TABLE_FIELDS = 'UPDATE {0} SET {1} WHERE {2}'

#twiter details:
# Constant app parameters from Mattan's account
TOKEN = "53083239-8DAIyzOOZQnUC2MHrJBWqMXXnTwipNwBWVVQS9e9C"
TOKEN_KEY = "NlK6AEVaOFocF6ZvXbww0qHq3w8e9TmckSBiwWKnXrXDC"
CON_SECRET = "8isQAuumhrcFY8Mv1A4v5CTWp"
CON_SECRET_KEY = "tevKUfyrpVc9V3pA1NtKUwRFEX2UI3TK0YAb3uzSkgvBtrmqSK"
CSV_PATH = r'../Utillities/Congress.csv'

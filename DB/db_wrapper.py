import mysql.connector as mdb
import consts


class DbWrapper():
    def __init__(self):
        self.open_connection()


    def open_connection(self):
        try:
            self.con = mdb.connect(user=consts.DB_USER, password=consts.DB_PASSWORD,
                                   host=consts.DB_HOSTNAME,
                                   database=consts.DB_NAME)
        except mdb.Error as err:
            if err.errno == mdb.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == mdb.errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)


    def close_connection(self):
        self.con.close()


    def get_values_by_id(self, table_name, id_value):
        pass

    def get_values_by_field(self, table_name, field_name, field_value):
        pass

    def get_num_of_rows(self, table_name):
        pass

    def insert_to_table(self, table_name, fields,values):
        pass
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
        cursor = self.con.cursor()
        query = consts.SELECT_BY_ID.format(table_name,id_value)
        cursor.execute()

        cursor.close()

    def get_values_by_field(self, table_name, field_name, field_value):
        pass

    def get_num_of_rows(self, table_name):
        pass

    def insert_to_table(self, table_name, fields,values):
        cursor = self.con.cursor()
        fileds_name = ''
        for field in fields:
            fileds_name+=field+','
        fileds_name = fileds_name[:-1]

        query = consts.INSERT_QUERY.format(table_name, fileds_name)
        values_tuple = tuple(values)
        query+='('
        for value in values:
            query+='%s,'

        query=query[:-1]
        query+=')'
        cursor.execute(query,values_tuple )
        self.con.commit()
        cursor.close()
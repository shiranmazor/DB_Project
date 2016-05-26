import mysql.connector as mdb
import consts
import traceback


class DbWrapper():
    def __init__(self, open_connection = True):
        if open_connection:
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
        cursor.execute(query)
        tuples = cursor.fetchall()
        cursor.close()
        return tuples

    def get_multiple_values_by_field(self, return_fileds,  table_name, field_name =None, field_value =None):
        try:
            cursor = self.con.cursor()
            query = 'select '
            for key in return_fileds:
                query+=key+','

            query = query[:-1]
            query+='from '+table_name
            if  field_name:
                values_tuple = (field_value,)
                query+='where '+field_name+'=%s'
                cursor.execute(query, values_tuple)
            else:
                cursor.execute(query)

            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
            cursor.close()
            return result
        except:
            print traceback.format_exc()

    def get_values_by_field(self, table_name, field_name, field_value):
        '''
        convert field_value to a tuple
        :param table_name:
        :param field_name:str
        :param field_value:str
        :return: list of dict
        '''
        try:
            cursor = self.con.cursor()
            values_tup = (field_value,)
            query = consts.SELECT_BY_FIELD.format(table_name,field_name,'%s')
            cursor.execute(query,values_tup)
            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
            cursor.close()
            return result
        except Exception as ex:
            print 'Error in selecting from db'
            print traceback.format_exc()

    def execute_generic_query(self, query):
        try:
            cursor = self.con.cursor()
            cursor.execute(query)
            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
            cursor.close()
            return result
        except:
            print traceback.format_exc()



    def get_num_of_rows(self, table_name):
        cursor = self.con.cursor()
        query = 'Select COUNT(*) from {0}'.format(table_name)
        cursor.execute(query)
        tuples = cursor.fetchall()
        cursor.close()
        return tuples

    def insert_to_table(self, table_name, fields,values):
        try:
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
        except Exception as ex:
            message = traceback.format_exc()
            if ('Duplicate entry' not in message ) and ('IntegrityError' not in message):
                print 'problem in inserting to DB! ,qeury won\'t be executed'
                print message




    def update_table(self, table_name, fields, values, condition_str):
        pass


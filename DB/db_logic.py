import db_wrapper
import traceback

class DBLogic():
    def __init__(self, db_wrapper_obj = None):
        if db_wrapper_obj:
            self.db_obj = db_wrapper_obj
        else:
            self.db_obj = db_wrapper.DbWrapper(open_connection = True)



    def get_lastest_tweet_date(self):
        query = 'select user_id, max(date) as latest_date from tweets group by User_id'
        outputs = self.db_obj.execute_generic_query(query)
        return outputs

    def get_user_ids(self):
        select_user_id = "select id from users"
        outputs = self.db_obj.execute_generic_query(select_user_id)
        return outputs

    def get_userid_screen_name_db(self):
        '''
        return dict with id and screen_name as keys
        :return:
        '''
        select_user_id = "select id,screen_name from users"
        outputs = self.db_obj.execute_generic_query(select_user_id)
        return outputs

    def get_user_id_by_name(self, full_name):
        try:

            cursor = self.db_obj.con.cursor()
            query = 'select id from users where full_name =%s'
            cursor.execute(query, (full_name,))
            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
            cursor.close()
            return result[0]['id']
        except:
            print traceback.format_exc()

    def get_last_id_from_table(self, table_name):
        query = 'select max(id) as last_id from {0}'.format(table_name)
        outputs = self.db_obj.execute_generic_query(query)
        return outputs

    def get_user_data_by_twitter_id(self,twitter_id):
        try:
            cursor = self.db_obj.con.cursor()
            query = "select * from users where twitter_id = %s"
            twitter_id = (twitter_id,)
            cursor.execute(query, twitter_id)
            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
            cursor.close()
            return result
        except:
            print traceback.format_exc()

    def get_latest_tweet_id(self, user_id, from_date):
        try:
            cursor = self.db_obj.con.cursor()
            query = ('select max(date), tweet_id from tweets where user_id = %s and date < %s')
            cursor.execute(query,(user_id,from_date))
            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
            cursor.close()
            return result
        except:
            print traceback.format_exc()


    def get_followers_name(self, user_id):
        '''
        contains complicated query
        :param user_id:
        :return:list of dicts with "full_name"
        '''
        try:
            cursor = self.db_obj.con.cursor()
            query = '''
            select users.full_name
            from users
            where id in
            (
            select follower_id
            from followers
            where followee_id = %s
            )
            '''
            cursor.execute(query, (user_id,))
            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
            cursor.close()
            return result

        except Exception as ex:
            print 'Error in selecting from db'
            print traceback.format_exc()

    def get_followees_name(self, user_id):
        '''
        contains complicated query
        :param user_id:
        :return:list of dicts with "full_name"
        '''
        try:
            cursor = self.db_obj.con.cursor()
            query = '''
            select users.full_name
            from users
            where id in
            (
            select followee_id
            from followers
            where follower_id = %s
            );
            '''
            cursor.execute(query, (user_id,))
            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
            cursor.close()
            return result

        except Exception as ex:
            print 'Error in selecting from db'
            print traceback.format_exc()

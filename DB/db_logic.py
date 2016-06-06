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

    def get_user_id_by_field(self, field_name, field_value):
        try:

            cursor = self.db_obj.con.cursor()
            query = 'select id from users where {0} =%s'.format(field_name)
            cursor.execute(query, (field_value,))
            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
            cursor.close()
            return result[0]['id']
        except:
            print traceback.format_exc()

    def get_full_names(self):
        query = 'select full_name from Users'
        outputs =  self.db_obj.execute_generic_query(query)
        lst = [x['full_name'] for x in outputs]
        return lst

    def get_user_id_by_fullname(self, full_name):
        user_output = self.db_obj.get_values_by_field(table_name='Users', field_name='full_name', field_value=full_name)
        result = [x['id'] for x in user_output]
        return result


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
            query = ('select max(date), tweet_id from tweets where user_id = %s and date >= %s')
            cursor.execute(query,(user_id,from_date))
            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
            cursor.close()
            return result
        except:
            print traceback.format_exc()

    def get_user_tweets(self, user_id):
        try:
            cursor = self.db_obj.con.cursor()
            query = ('select * from tweets where user_id = %s ')
            cursor.execute(query, (user_id, ))
            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
            cursor.close()
            return result
        except:
            print traceback.format_exc()



    def get_followers_screen_name(self, user_id):
        '''
        contains complicated query
        :param user_id:
        :return:list of dicts with "full_name"
        '''
        try:
            cursor = self.db_obj.con.cursor()
            query = '''
            select users.screen_name
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

    def get_followees_screen_name(self, user_id):
        '''
        contains complicated query
        :param user_id:
        :return:list of dicts with "full_name"
        '''
        try:
            cursor = self.db_obj.con.cursor()
            query = '''
            select users.screen_name
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

    def get_users_list_with_party(self):
        try:
            cursor = self.db_obj.con.cursor()
            query = '''
            select u.id as id, u.screen_name as screen_name, u.full_name as full_name, u.location as state,
             p.party_name as party_name, r.rol_name as role_name
            from users as u, party as p, role as r
            where u.party_id = p.party_id
            and u.role_id = r.role_id
            '''
            cursor.execute(query)
            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
            cursor.close()
            return result

        except Exception as ex:
            print 'Error in selecting from db'
            print traceback.format_exc()

    def get_mentions_userid(self, tweet_id):
        try:
            cursor = self.db_obj.con.cursor()
            query = '''
            select tagged_users_id
            from mentions
            where tweet_id = %s
            '''
            cursor.execute(query, (tweet_id,))
            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
            cursor.close()
            return result

        except Exception as ex:
            print 'Error in selecting from db'
            print traceback.format_exc()

    def get_searches_by_id(self, user_id):
        try:
            cursor = self.db_obj.con.cursor()
            query = '''
            select *
            from searches
            where user_id = %s
            '''
            cursor.execute(query, (user_id,))
            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
            cursor.close()
            return result

        except Exception as ex:
            print 'Error in selecting from db'
            print traceback.format_exc()

    def get_tweet_files(self, tweet_id):
        try:
            cursor = self.db_obj.con.cursor()
            query = '''
            select *
            from tweet_files
            where tweets_id = %s
            '''
            cursor.execute(query, (tweet_id,))
            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
            cursor.close()
            return result

        except Exception as ex:
            print 'Error in selecting from db'
            print traceback.format_exc()

    def get_popular_searches(self, count=10):
        try:
            cursor = self.db_obj.con.cursor()
            query = '''
            select * from searches
            order by count desc
            limit %s
            '''
            cursor.execute(query, (count,))
            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
            cursor.close()
            return result

        except Exception as ex:
            print 'Error in selecting from db'
            print traceback.format_exc()

    def get_last_tweet_date(self,screen_name):
        try:
            cursor = self.db_obj.con.cursor()
            query = '''
            select max(t.date) as date
            from tweets as t, users as u
            where t.user_id = u.id
            and u.screen_name = %s
            '''
            values = (screen_name,)
            cursor.execute(query, values)
            columns = cursor.description
            result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
            cursor.close()
            if len(result) > 0:
                return result[0]['date']
            else:
                return None

        except Exception as ex:
            print 'Error in selecting from db'
            print traceback.format_exc()


    def get_popularity_users(self):
        '''
        this function execute a complex qeury - returning the user with maximum followers num
        with his search data - how many times he is being search and when was the last time
        :return: list of dicts, every dict contain keys: user_id,name,screen_name,last_search,num_of_searches,followers_count
        '''
        complex_query1 = '''
            select searches.user_id as user_id,users.full_name as name, users.screen_name as screen_name, searches.last_date as last_search
            , searches.count as num_of_searches
            from searches , users
            where searches.user_id = users.id
            and searches.user_id in
            (
            select follow2.followee_id
            from
                (
                select follow.followee_id, max(followers_num) as followers_count
                from
                    (
                    select followee_id, count(follower_id) as followers_num
                    from followers
                    group by followee_id
                    ) as follow
                ) as follow2
            )
        '''
        get_max_followers_count_query = '''
        select  max(followers_num) as followers_count
        from
            (
            select followee_id, count(follower_id) as followers_num
            from followers
            group by followee_id
            ) as follow
        '''
        output1 = self.db_obj.execute_generic_query(complex_query1)
        output2 = self.db_obj.execute_generic_query(get_max_followers_count_query)[0]
        for out in output1:
            out['followers_count'] = output2['followers_count']

        return output1
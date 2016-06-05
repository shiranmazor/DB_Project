--check how many records exist on db:
SELECT SUM(TABLE_ROWS)
     FROM INFORMATION_SCHEMA.TABLES
     WHERE TABLE_SCHEMA = 'hoc_db';

---create index on screen_name in users table
CREATE INDEX screen_name_index ON  users(screen_name) USING BTREE;
---create index on full_name in users table
CREATE INDEX full_name_index ON  users(full_name) USING BTREE;


ALTER DATABASE hoc_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

--complex sql query:
--1. getting the followee_id of the user wuth maximun followers in our system:
select follow.followee_id, max(followers_num) as followers_count
from
(
select followee_id, count(follower_id) as followers_num
from followers
group by followee_id
) as follow

--2. num of searches
select s.count
from searches as s
where s.user_id in
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

--2. getting the user_id, full_name, screen_name, search count, followers count of the populaar user

select u.id, u.screen_name, u.full_name, ss.user_id

select s.user_id s.count , follow2.followers_count
from searches as s
where s.user_id in
(
select follow2.followee_id , follow2.followers_count
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
) as ss
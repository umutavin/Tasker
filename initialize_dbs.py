import psycopg2 as dbconnector
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

con = dbconnector.connect("dbname='postgres' user='postgres' host='localhost' password='postgres'")
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = con.cursor()


# CREATE DATABASES
def create_users_db(cur):
	que = """CREATE DATABASE TASKERDB;"""
	cur.execute(que)


# CREATE TABLES
def create_tables():
	connection_string = "dbname='taskerdb' user='tasker' host='localhost' password='tasker'"
	with dbconnector.connect(connection_string) as connection:
		cur = connection.cursor()
		create_users_table(cur)
		create_teams_table(cur)
		create_teamuserrelations_table(cur)
		create_roles_table(cur)
		create_userrolerelations_table(cur)
		create_projects_table(cur)
		create_projectteamrelations_table(cur)
		create_tasks_table(cur)
		create_taskuserrelations_table(cur)


def create_users_table(cur):
	que = """CREATE TABLE IF NOT EXISTS USERS(
		id SERIAL PRIMARY KEY,
		username VARCHAR(50) UNIQUE NOT NULL,
		salt VARCHAR(40) UNIQUE NOT NULL,
		hash VARCHAR(64) NOT NULL,
		email VARCHAR(40) UNIQUE NOT NULL,
		name VARCHAR(20) NOT NULL,
		surname VARCHAR(20) NOT NULL,
		profile_pic VARCHAR(40)
	)
	"""
	cur.execute(que)


def create_teams_table(cur):
	que = """CREATE TABLE IF NOT EXISTS TEAMS(
		id SERIAL PRIMARY KEY,
		name VARCHAR(50) NOT NULL
		)
	"""
	cur.execute(que)


def create_teamuserrelations_table(cur):
	que = """CREATE TABLE IF NOT EXISTS TEAM_USER_RELATIONS(
		id SERIAL PRIMARY KEY,
		team_id INTEGER REFERENCES TEAMS(id) ON DELETE CASCADE,
		user_id INTEGER REFERENCES USERS(id) ON DELETE CASCADE
	)
	"""
	cur.execute(que)


def create_roles_table(cur):
	que = """CREATE TABLE IF NOT EXISTS ROLES(
		id SERIAL PRIMARY KEY,
		name VARCHAR(20) NOT NULL,
		description VARCHAR(255)
	)
	"""
	cur.execute(que)


def create_userrolerelations_table(cur):
	que = """CREATE TABLE IF NOT EXISTS USER_ROLE_RELATIONS(
		id SERIAL PRIMARY KEY,
		teamuser_id INTEGER REFERENCES TEAM_USER_RELATIONS(id) ON DELETE CASCADE,
		role_id INTEGER REFERENCES ROLES(id) ON DELETE CASCADE
	)
	"""
	cur.execute(que)


def create_projects_table(cur):
	que = """CREATE TABLE IF NOT EXISTS PROJECTS(
		id SERIAL PRIMARY KEY,
		name VARCHAR(50) NOT NULL,
		budget INTEGER NOT NULL,
		status INTEGER NOT NULL,
		scheduled_time date NOT NULL,
		description VARCHAR(255)
	)
	"""
	cur.execute(que)


def create_projectteamrelations_table(cur):
	que = """CREATE TABLE IF NOT EXISTS PROJECT_TEAM_RELATIONS(
		id SERIAL PRIMARY KEY,
		project_id INTEGER REFERENCES PROJECTS(id) ON DELETE CASCADE,
		team_id INTEGER REFERENCES TEAMS(id) ON DELETE CASCADE
	)
	"""
	cur.execute(que)


def create_tasks_table(cur):
	que = """CREATE TABLE IF NOT EXISTS TASKS(
		id SERIAL PRIMARY KEY,
		name VARCHAR(30) NOT NULL,
		status INTEGER DEFAULT 0,
		project_id INTEGER REFERENCES PROJECTS(id) ON DELETE CASCADE,
		description VARCHAR(255)
	)
	"""
	cur.execute(que)


def create_taskuserrelations_table(cur):
	que = """CREATE TABLE IF NOT EXISTS TASK_USER_RELATIONS(
		id SERIAL PRIMARY KEY,
		user_id INTEGER REFERENCES USERS(id) ON DELETE CASCADE,
		task_id INTEGER REFERENCES TASKS(id) ON DELETE CASCADE
	)
	"""
	cur.execute(que)

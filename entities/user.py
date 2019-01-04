import hashlib
import random
import crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired


class User:
	def __init__(self, id, username, password, email, name, surname, profile_pic):
		self.id = id
		self.username = username
		self.password = password
		self.email = email
		self.name = name
		self.surname = surname
		self.profile_pic = profile_pic
	
	def generate_auth_token(self, app, expiration = 600):
		s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
		return s.dumps({'id': self.id})

def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None
    except BadSignature:
        return None
    return data['id']

def create_random_salt():
	salt = crypt.mksalt(crypt.METHOD_SHA256)
	return salt[:40]

def create_hash(salt, password):
	hash_object = hashlib.sha256(password.encode() + salt.encode())
	return hash_object.hexdigest()

#USER TABLE OPERATIONS
def create_user(cur, user):
	que = """INSERT INTO 
	USERS (username, salt, hash, email, name, surname) 
	VALUES(%(username)s, %(salt)s, %(hash)s, %(email)s, %(name)s, %(surname)s)
	"""
	salt = create_random_salt()
	hash = create_hash(salt, user.password)
	cur.execute(que, {'username':user.username, 'salt':salt, 'hash':hash, 'email':user.email, 'name':user.name, 'surname':user.surname})

def get_user(cur, username):
	#returns user as array
	que = """SELECT * FROM USERS WHERE (username = %(username)s)"""
	cur.execute(que, {'username':username})
	if cur.rowcount <= 0:
		return 0, "", "", "", "", "", "", ""
	else:
		return cur.fetchone() 

def get_user_by_id(cur, id):
	que = """SELECT * FROM USERS WHERE (id = %(id)s)"""
	cur.execute(que, {'id':id})
	if cur.rowcount <= 0:
		return 0, "", "", "", "", "", "", ""
	else:
		return cur.fetchone() 

def get_user_teams(cur, userId):
	#returns a user's team and role information
	que = """SELECT U.id, T.name, R.name FROM USERS U, TEAMS T, TEAM_USER_RELATIONS TU, ROLES R, USER_ROLE_RELATIONS UR 
	WHERE U.id = TU.user_id 
	AND TU.team_id = T.id
	AND TU.id = UR.teamuser_id
	AND R.id = TU.role_id
	AND U.id = %(id)s"""
	cur.execute(que, {'id':userId})
	return cur.fetchall()

def get_user_projects(cur, userId):
	#returns a user's project and task information
	que = """SELECT U.id, T.id, T.name, P.id, P.name, TA.id, TA.name, TA.description, TA.status FROM USERS U, TASK_USER_RELATIONS TAU, TASKS TA, PROJECTS P, TEAMS T, PROJECT_TEAM_RELATIONS PT
	WHERE U.id = TAU.user_id
	AND TAU.task_id = TA.id
	AND TA.project_id = P.id
	AND P.id = PT.project_id
	AND PT.team_id = T.id
	AND U.id = %(id)s"""
	cur.execute(que, {'id':userId})
	return cur.fetchall()

def get_all_users(cur):
	que = """SELECT * FROM USERS"""
	cur.execute(que)
	return cur.fetchall()

def get_all_usernames(cur):
	que = """SELECT id, username FROM USERS"""
	cur.execute(que)
	return cur.fetchall()

def search_users(cur, username):
	que = """SELECT * FROM USERS WHERE (username LIKE %%%(username)s%%)"""
	cur.execute(que, {'username':username})
	return cur.fetchall()

def delete_user(cur, username):
	que = """DELETE FROM USERS WHERE (username = %(username)s)"""
	cur.execıte(que, {'username':username})

def update_user(cur, user):
	que = """UPDATE USERS SET username = %(username)s, 
		salt = %(salt)s, hash = %(hash)s, email = %(email)s, 
		name = %(name)s, surname = %(surname)s 
		WHERE (id = %(id)s)
	"""
	salt = create_random_salt()
	hash = create_hash(salt, user.password)
	cur.execute(que, {'id':user.id ,'username':user.username, 'salt':salt, 'hash':hash, 'email':user.email, 'name':user.name, 'surname':user.surname})
	
class Team:
	def __init__(self, id, name):
		self.id = id
		self.name = name


class TeamMember:
    def __init__(self, teamId, userId):
        self.teamId=teamId
        self.userId=userId


def create_team(cur, team):
	que = """INSERT INTO
	TEAMS (name)
	VALUES(%(name)s)
	"""
	cur.execute(que, {'name':team.name})

def delete_team(cur, id):
    que = """DELETE FROM TEAMS WHERE id = %(id)s"""
    cur.execute(que, {'id':id})

def add_user_to_team(cur, team_id, user_id):
    que = """INSERT INTO TEAM_USER_RELATIONS(team_id, user_id)
        SELECT %(teamId)s, %(userId)s WHERE NOT EXISTS (SELECT team_id, user_id FROM team_user_relations WHERE team_id=%(teamId)s AND user_id=%(userId)s);
    """
    cur.execute(que, {'teamId':team_id, 'userId':user_id})

def get_team_members(cur, team_id):
    que = """SELECT TU.id, U.username, U.email, U.name, U.surname FROM USERS U, TEAM_USER_RELATIONS TU WHERE U.id = TU.user_id AND TU.team_id = %(team_id)s
    """
    cur.execute(que, {'team_id':team_id})
    return cur.fetchall()

def delete_user_from_team(cur, id):
    que = """DELETE FROM TEAM_USER_RELATIONS WHERE id = %(id)s"""
    cur.execute(que, {'id':id})

def update_team(cur, team):
    que = """UPDATE TEAMS SET name = %(name)s WHERE id = %(id)s"""
    cur.execute(que, {'name':team.name, 'id':team.id})

def get_all_teams(cur):
    que = """SELECT * FROM TEAMS"""
    cur.execute(que)
    return cur.fetchall()

def get_team(cur, id):
    que = """SELECT * FROM TEAMS WHERE id = %(id)s"""
    cur.execute(que, {'id':id})
    return cur.fetchall()

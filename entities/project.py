class Project:
    def __init__(self, id, name, budget, status, scheduled_time, description):
        self.id = id
        self.name = name
        self.budget = budget
        self.status = status
        self.scheduled_time = scheduled_time
        self.description = description

def create_project(cur, project):
    que = """INSERT INTO PROJECTS (name, budget, status, scheduled_time, description)
    VALUES (%(name)s, %(budget)s, %(status)s, %(scheduled_time)s, %(description)s)"""
    cur.execute(que, {'name':project.name, 'budget':project.budget, 'status':project.status, 'scheduled_time':project.scheduled_time, 'description':project.description})

def update_project(cur, project):
    que = """UPDATE PROJECTS SET name = %(name)s, budget = %(budget)s, status = %(status)s, scheduled_time = %(scheduled_time)s, description = %(description)s 
    WHERE id = %(id)s"""
    cur.execute(que, {'name':project.name, 'budget':project.budget, 'status':project.status, 'scheduled_time':project.scheduled_time, 'description':project.description, 'id':project.id})

def add_team_to_project(cur, project_id, team_id):
    que = """INSERT INTO PROJECT_TEAM_RELATIONS (project_id, team_id)
    VALUES (%(project_id)s, %(team_id)s)"""
    cur.execute(que, {'project_id':project_id, 'team_id':team_id})

def remove_team_from_project(cur, project_id, team_id):
    que = """DELETE FROM PROJECT_TEAM_RELATIONS WHERE project_id = %(project_id)s AND team_id = %(team_id)s"""
    cur.execute(que, {'project_id':project_id, 'team_id':team_id})

def get_project(cur, id):
    que = """SELECT * FROM PROJECTS WHERE id = %(id)s"""
    cur.execute(que, {'id':id})
    return cur.fetchall()

def get_all_projects(cur):
    que = """SELECT * FROM PROJECTS"""
    cur.execute(que)
    return cur.fetchall()

def get_notstarted_projects(cur):
    que = """SELECT * FROM PROJECTS WHERE status=0"""
    cur.execute(que)
    return cur.fetchall()

def get_ongoing_projects(cur):
    que = """SELECT * FROM PROJECTS WHERE status=1"""
    cur.execute(que)
    return cur.fetchall()

def get_completed_projects(cur):
    que = """SELECT * FROM PROJECTS WHERE status=2"""
    cur.execute(que)
    return cur.fetchall()

def get_project_teams(cur, project_id):
    que = """SELECT T.name FROM TEAMS T, PROJECT_TEAM_RELATIONS PT WHERE T.id = PT.team_id AND PT.project_id = %(project_id)s
    """
    cur.execute(que, {'project_id':project_id})
    return cur.fetchall()


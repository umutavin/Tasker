class Task:
    def __init__(self, id, name, desc, project_id, status):
        self.id = id
        self.name = name
        self.desc = desc
        self.project_id = project_id
        self.status = status
        self.task_type = "CreateTask"

def create_task(cur, task):
    que = """INSERT INTO TASKS (name, status, project_id, description)
    VALUES (%(name)s, %(status)s, %(project_id)s, %(description)s)"""
    cur.execute(que, {'name':task.name, 'status':task.status, 'project_id':task.project_id, 'description':task.desc})

def delete_task(cur, id):
    que = """DELETE FROM TASKS WHERE id = %(id)s"""
    cur.execute(que, {'id':id})

def update_task(cur, task):
    que = """UPDATE TASKS SET name = %(name)s, description = %(description)s, project_id = %(project_id)s, status = %(status)s WHERE id = %(id)s"""
    cur.execute(que, {'name':task.name, 'description':task.desc, 'project_id':task.project_id, 'status':task.status, 'id':task.id})

def get_project_tasks(cur, project_id):
    que = """SELECT A.*, U.username FROM (SELECT T.*, TU.user_id FROM (SELECT * FROM TASKS WHERE project_id = %(project_id)s) T LEFT JOIN TASK_USER_RELATIONS TU ON t.id = TU.task_id) A LEFT JOIN USERS U ON U.id = A.user_id"""
    cur.execute(que, {'project_id':project_id})
    return cur.fetchall()

def assign_task_to_user(cur, user_id, task_id):
    que = """INSERT INTO TASK_USER_RELATIONS (user_id, task_id)
    VALUES (%(user_id)s, %(task_id)s)"""
    cur.execute(que, {'user_id':user_id, 'task_id':task_id})

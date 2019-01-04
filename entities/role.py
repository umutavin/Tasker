class Role:
    def __init__(self, id, name, desc):
        self.id = id
        self.name = name
        self.desc = desc

def create_role(cur, role):
    que = """INSERT INTO 
    ROLES (name, description)
    VALUES (%(name)s, %(description)s"""
    cur.execute(que, {'name':role.name, 'description':role.desc})

def add_role_to_teamuser(cur, teamuser_id, role_id):
    que = """INSERT INTO USER_ROLE_RELATIONS (teamuser_id, role_id)
    VALUES (%(teamuser_id)s, %(role_id)s)
    """
    cur.execute(que, {'teamuser_id':teamuser_id, 'role_id':role_id})

def remove_role_from_teamuser(cur, teamuser_id, role_id):
    que = """DELETE FROM USER_ROLE_RELATIONS WHERE teamuser_id = %(teamuser_id)s AND role_id = %(role_id)s"""
    cur.execute(que, {'teamuser_id':teamuser_id, 'role_id':role_id})

def update_role(cur, role):
    que = """UPDATE ROLES SET name = %(name)s, description = %(description)s WHERE id = %(id)s"""
    cur.execute(que, {'name':role.name, 'description':role.desc, 'id':role.id})

def get_all_roles(cur):
    que = """SELECT * FROM ROLES"""
    cur.execute(que)
    return cur.fetchall()


from flask import Flask, request
import psycopg2 as dbconnector
import json
from entities.project import *
from entities.task import *
import datetime 

app = Flask(__name__)
app.secret_key = '+_9o$w9+9xro!-y(wvuv+vvyc!$x(@ak(!oh@ih0ul+6cf=$f'


def date2str(o):
    if isinstance(o, datetime.date):
        return o.__str__()


def str2date(o):
    return datetime.datetime.strptime(o, '%Y-%m-%d').date()


@app.route('/api/projects', methods=['GET', 'POST'])
def projects_page():
    if request.method == "POST":
        data = request.data.decode()
        data = json.loads(data)
        project_id = data['id']
        project_name = data['name']
        project_budget = data['budget']
        project_status = data['status']
        project_scheduled_time = str2date(data['scheduled_time'])
        project_description = data['description']

        added_project = Project(project_id, project_name, project_budget, project_status, project_scheduled_time, project_description)
        try:
            connection = dbconnector.connect("dbname='taskerdb' user='tasker' host='localhost' password='tasker'")
            cursor = connection.cursor()
            create_project(cursor, added_project)
        except dbconnector.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        try:
            connection = dbconnector.connect("dbname='taskerdb' user='tasker' host='localhost' password='tasker'")
            cursor = connection.cursor()
            projects_list = get_all_projects(cursor)
        except dbconnector.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
            return json.dumps([list(elem) for elem in projects_list], default=date2str)


@app.route('/api/projects/not_started')
def notstarted_projects_page():
    try:
        connection = dbconnector.connect("dbname='taskerdb' user='tasker' host='localhost' password='tasker'")
        cursor = connection.cursor()
        projects_list = get_notstarted_projects(cursor)
    except dbconnector.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.commit()
        connection.close()
        return json.dumps([list(elem) for elem in projects_list], default=date2str)


@app.route('/api/projects/ongoing')
def ongoing_projects_page():
    try:
        connection = dbconnector.connect("dbname='taskerdb' user='tasker' host='localhost' password='tasker'")
        cursor = connection.cursor()
        projects_list = get_ongoing_projects(cursor)
    except dbconnector.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.commit()
        connection.close()
        return json.dumps([list(elem) for elem in projects_list], default=date2str)


@app.route('/api/projects/completed')
def completed_projects_page():
    try:
        connection = dbconnector.connect("dbname='taskerdb' user='tasker' host='localhost' password='tasker'")
        cursor = connection.cursor()
        projects_list = get_completed_projects(cursor)
    except dbconnector.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.commit()
        connection.close()
        return json.dumps([list(elem) for elem in projects_list], default=date2str)


@app.route('/api/projects/<string:projectId>', methods=['GET', 'POST'])
def project_details(projectId):
    if request.method == "POST":
        data = request.data.decode()
        data = json.loads(data)
        project_id = data['id']
        project_name = data['name']
        project_budget = data['budget']
        project_status = data['status']
        project_scheduled_time = str2date(data['scheduled_time']) if data['scheduled_time'] != '' else ''
        project_description = data['description']
        try:
            connection = dbconnector.connect("dbname='taskerdb' user='tasker' host='localhost' password='tasker'")
            cursor = connection.cursor()

            if not project_name:
                statement = """SELECT name FROM projects where ID = %s"""
                cursor.execute(statement, projectId)
                project_name = cursor.fetchone()
            if not project_budget:
                statement = """SELECT budget FROM projects where ID = %s"""
                cursor.execute(statement, projectId)
                project_budget = cursor.fetchone()
            if not project_status:
                statement = """SELECT status FROM projects where ID = %s"""
                cursor.execute(statement, projectId)
            if not project_scheduled_time:
                statement = """SELECT scheduled_time FROM projects where ID = %s"""
                cursor.execute(statement, projectId)
                project_scheduled_time = cursor.fetchone()
            if not project_description:
                statement = """SELECT description FROM projects where ID = %s"""
                cursor.execute(statement, projectId)
                project_description = cursor.fetchone()
            updated_project = Project(1, project_name, project_budget, project_status, project_scheduled_time, project_description)
            update_project(cursor, updated_project)
        except dbconnector.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        try:
            connection = dbconnector.connect("dbname='taskerdb' user='tasker' host='localhost' password='tasker'")
            cursor = connection.cursor()
            project = get_project(cursor, projectId)
        except dbconnector.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
            return json.dumps(list(project), default=date2str)


@app.route('/api/projects/<string:projectId>/tasks', methods=['GET', 'POST'])
def tasks_page(projectId):
    if request.method == "POST":
        data = request.data.decode()
        data = json.loads(data)
        formtype = data['task_type']
        if formtype == 'CreateTask':
            task_name = data['name']
            task_status = data['status']
            task_description = data['desc']
            project_id = data['project_id']
            added_task = Task(1, task_name, task_description, projectId, task_status)
            try:
                connection = dbconnector.connect("dbname='taskerdb' user='tasker' host='localhost' password='tasker'")
                cursor = connection.cursor()
                create_task(cursor, added_task)
            except dbconnector.Error as e:
                print(e.pgerror)
                connection.rollback()
            finally:
                connection.commit()
                connection.close()
                return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        elif formtype == 'UpdateTask':
            try:
                taskId = data['id']
                task_name = data['name']
                task_status = data['status']
                task_description = data['desc']
                project_id = data['project_id']
                connection = dbconnector.connect("dbname='taskerdb' user='tasker' host='localhost' password='tasker'")
                cursor = connection.cursor()
                if not task_name:
                    statement = """SELECT name FROM tasks where PROJECT_ID = %s"""
                    cursor.execute(statement, projectId)
                    task_name = cursor.fetchone()
                if not task_status:
                    statement = """SELECT status FROM tasks where PROJECT_ID = %s"""
                    cursor.execute(statement, projectId)
                    task_status = cursor.fetchone()
                if not task_description:
                    statement = """SELECT description FROM tasks where PROJECT_ID = %s"""
                    cursor.execute(statement, projectId)
                    task_description = cursor.fetchone()
                updated_task = Task(taskId, task_name, task_description, project_id, task_status)
                update_task(cursor, updated_task)
            except dbconnector.Error as e:
                print(e.pgerror)
                connection.rollback()
            finally:
                connection.commit()
                connection.close()
                return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    else:
        try:
            connection = dbconnector.connect("dbname='taskerdb' user='tasker' host='localhost' password='tasker'")
            cursor = connection.cursor()
            task_list = get_project_tasks(cursor, projectId)
        except dbconnector.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
            return json.dumps([list(elem) for elem in task_list], default=date2str)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)

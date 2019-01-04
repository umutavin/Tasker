from flask import Flask, render_template, request, redirect, jsonify, g
from flask_httpauth import HTTPBasicAuth
from flask.helpers import url_for
import psycopg2 as dbconnector
from flask.globals import session
from entities.user import *
from entities.project import *
from entities.task import *
from entities.team import *
import datetime, json, requests, base64

auth = HTTPBasicAuth()
app = Flask(__name__)
app.secret_key = '+_9o$w9+9xro!-y(wvuv+vvyc!$x(@ak(!oh@ih0ul+6cf=$f'


def str2date(o):
    return datetime.datetime.strptime(o, '%Y-%m-%d').date()


def welcome_pages():
    pages_list = []
    if 'logged_in' in session and session['logged_in']:
        welcome_msg = "Welcome, " + session['username'] + "!"
        pages_list.append(dict(title='Logout', href='/logout'))
    else:
        welcome_msg = "Not logged in yet. Please log in."
        pages_list.append(dict(title='Register', href='/register'))
        pages_list.append(dict(title='Login', href='/login'))
    return pages_list, welcome_msg


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(app, 600)
    return jsonify({'token': token.decode('ascii')})


@auth.verify_password
def verify_password(username_or_token, password):
# first try to authenticate by token
    connection = dbconnector.connect("dbname='taskerdb' user='tasker' host='localhost' password='tasker'")
    cursor = connection.cursor()
    userid = verify_auth_token(username_or_token)
    if userid == None:
        userid = -1
    _, username, salt, hash, email, name, surname, profile_pic = get_user_by_id(cursor, userid)
    if not username:
        # try to authenticate with username/password
        user_id, username, salt, hash, email, name, surname, profile_pic = get_user(cursor, username_or_token)
        createdHash = create_hash(salt, password)
        if hash != createdHash:
            return False
        else:
            user = User(user_id, username, password, email, name, surname, profile_pic)
    else:
        user = User(userid, username, password, email, name, surname, profile_pic)
    g.user = user
    return True


@app.route('/')
def home_page():
    pages_list, welcome_msg = welcome_pages()
    return render_template('home.html', pages=pages_list, welcome_msg=welcome_msg)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    try:
        connection = dbconnector.connect("dbname='taskerdb' user='tasker' host='localhost' password='tasker'")
        cursor = connection.cursor()
        try:
            if request.method == 'POST':
                if "add" in request.form:
                    user = User(0, request.form['username'], request.form['password'], request.form['email'], request.form['name'], request.form['surname'], "")
                    create_user(cursor, user)
                    return render_template('register.html')
            else:
                if 'logged_in' in session and session['logged_in'] == True:
                    return redirect(url_for('home_page'))
                else:
                    return render_template('register.html')
        except dbconnector.Error as e:
                print(e.pgerror)
    except dbconnector.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.commit()
        connection.close()
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            credentials = username + ':' + password
            headers = {'content-type': 'application/json', 'Authorization': 'Basic %s' % base64.b64encode(credentials.encode()).decode()}
            response = requests.get('http://0.0.0.0:5500/api/get_username', headers=headers)
            if response.content.decode() != "Unauthorized Access":
                if response.json()['username'] == username:
                    session['logged_in'] = True
                    session['user_id'] = response.json()['id']
                    session['username'] = response.json()['username']
                    return redirect(url_for('home_page'))
                else:
                    return render_template('login.html', isAlert=True, alertMessage='Username or password is invalid.')
            else:
                return render_template('login.html', isAlert=True, alertMessage='Username or password is invalid.')
        elif 'logged_in' in session and session['logged_in'] == True:
            return redirect(url_for('home_page'))
        else:
            return render_template('login.html', isAlert=False, alertMessage='')
    except dbconnector.Error as e:
        print(e.pgerror)


@app.route('/logout', methods=['GET', 'POST'])
def logout_page():
    if 'logged_in' in session and session['logged_in'] == True:
        session['logged_in'] = False
        session['username'] = ""
        session['userId'] = 0
    return redirect(url_for('home_page'))


@app.route('/projects', methods=['GET', 'POST'])
def projects_page():
    if request.method == "POST":
        project_name = request.form['ProjectName']
        project_budget = request.form['ProjectBudget']
        project_status = request.form['ProjectStatus']
        project_scheduled_time = request.form['ProjectScheduledTime']
        project_description = request.form['ProjectDescription']

        added_project = Project(1, project_name, project_budget, project_status, project_scheduled_time,
                                project_description)
        added_project_json = json.dumps(added_project.__dict__)
        try:
            requests.post('http://0.0.0.0:5001/api/projects', data=added_project_json)
        except dbconnector.Error as e:
            print(e.pgerror)
        finally:
            return redirect(url_for('projects_page'))
    else:
        projects_list = requests.get('http://0.0.0.0:5001/api/projects').json()
        for p in projects_list:
            p[4] = str2date(p[4])
        pages_list, welcome_msg = welcome_pages()
        return render_template('projects.html', pages=pages_list, projects=projects_list, welcome_msg=welcome_msg)


@app.route('/projects/not_started')
def notstarted_projects_page():
    projects_list = requests.get('http://0.0.0.0:5001/api/projects/not_started').json()
    for p in projects_list:
        p[4] = str2date(p[4])
    pages_list, welcome_msg = welcome_pages()
    return render_template('projects.html', pages=pages_list, projects=projects_list, welcome_msg=welcome_msg)


@app.route('/projects/ongoing')
def ongoing_projects_page():
    projects_list = requests.get('http://0.0.0.0:5001/api/projects/ongoing').json()
    for p in projects_list:
        p[4] = str2date(p[4])
    pages_list, welcome_msg = welcome_pages()
    return render_template('projects.html', pages=pages_list, projects=projects_list, welcome_msg=welcome_msg)


@app.route('/projects/completed')
def finished_projects_page():
    projects_list = requests.get('http://0.0.0.0:5001/api/projects/completed').json()
    for p in projects_list:
        p[4] = str2date(p[4])
    pages_list, welcome_msg = welcome_pages()
    return render_template('projects_completed.html', pages=pages_list, projects=projects_list, welcome_msg=welcome_msg)


@app.route('/projects/<string:projectId>', methods=['GET', 'POST'])
def project_details(projectId):
    if request.method == "POST":
        project_name = request.form['ProjectName']
        project_budget = request.form['ProjectBudget']
        project_status = request.form['ProjectStatus']
        project_scheduled_time = request.form['ProjectScheduledTime']
        project_description = request.form['ProjectDescription']

        updated_project = Project(projectId, project_name, project_budget, project_status, project_scheduled_time,
                                  project_description)
        updated_project_json = json.dumps(updated_project.__dict__)
        try:
            requests.post('http://0.0.0.0:5001/api/projects/' + projectId, data=updated_project_json)
        except dbconnector.Error as e:
            print(e.pgerror)
        finally:
            return redirect(url_for('project_details', projectId=projectId))
    else:
        project = requests.get('http://0.0.0.0:5001/api/projects/' + projectId).json()
        pages_list, welcome_msg = welcome_pages()
        return render_template('project_details.html', pages=pages_list, project=project, welcome_msg=welcome_msg)


@app.route('/projects/<string:projectId>/tasks', methods=['GET', 'POST'])
def tasks_page(projectId):
    if request.method == "POST":
        formtype = request.form['form-name']
        task_name = request.form['TaskName']
        task_status = request.form['TaskStatus']
        task_description = request.form['TaskDescription']
        projectId = request.form['projectId']
        added_task = Task(1, task_name, task_description, projectId, task_status)
        if formtype == 'UpdateTask':
            added_task.task_type = 'UpdateTask'
        task_json = json.dumps(added_task.__dict__)
        try:
            requests.post('http://0.0.0.0:5001/api/projects/'+projectId+'/tasks', data=task_json)
        except dbconnector.Error as e:
            print(e.pgerror)
        finally:
            return redirect(url_for('tasks_page', projectId=projectId))
    else:
        task_list = requests.get('http://0.0.0.0:5001/api/projects/'+projectId+'/tasks').json()
        pages_list, welcome_msg = welcome_pages()  # ?????
        return render_template('tasks.html', pages=pages_list, tasks=task_list, projectId=projectId, welcome_msg=welcome_msg)


@app.route('/teams', methods=['GET', 'POST'])
def teams_page():
    if request.method == "POST":
        team_name = request.form['TeamName']
        added_team = Team(1, team_name)
        added_team_json = json.dumps(added_team.__dict__)
        try:
            requests.post('http://0.0.0.0:5002/api/teams', data=added_team_json)
        except dbconnector.Error as e:
            print(e.pgerror)
        finally:
            return redirect(url_for('teams_page'))
    else:
        teams_list = requests.get('http://0.0.0.0:5002/api/teams').json()
        pages_list, welcome_msg = welcome_pages()
        return render_template('teams.html', pages=pages_list, teams=teams_list, welcome_msg=welcome_msg)


@app.route('/teams/<string:teamId>', methods=['GET', 'POST'])
def team_details(teamId):
    if request.method == "POST":
        user_id = request.form['id']
        team_member = TeamMember(teamId, user_id)
        team_member_json = json.dumps(team_member.__dict__)
        try:
            requests.post('http://0.0.0.0:5002/api/teams/' + teamId, data=team_member_json)
        except dbconnector.Error as e:
            print(e.pgerror)
        finally:
            return redirect(url_for('team_details', teamId=teamId))
    else:
        try:
            connection = dbconnector.connect("dbname='taskerdb' user='tasker' host='localhost' password='tasker'")
            cursor = connection.cursor()
            team = get_team(cursor, teamId)
            teammembers = requests.get('http://0.0.0.0:5002/api/teams/' + teamId).json()
            users = get_all_usernames(cursor)
        except dbconnector.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
        pages_list, welcome_msg = welcome_pages()
        return render_template('team_details.html', pages=pages_list, team=team, welcome_msg=welcome_msg, users=users,
                               teammembers=teammembers)


@app.route('/removeteammember/id=<string:relation_id>&team_id=<string:team_id>', methods=['POST', 'GET'])
def remove_member_from_team(relation_id, team_id):
    message = requests.get('http://0.0.0.0:5002/api/removeteammember/id=' + relation_id).json()
    return redirect(url_for('team_details', teamId=team_id))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

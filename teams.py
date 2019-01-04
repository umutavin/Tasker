from flask import Flask, request
import psycopg2 as dbconnector
import json 
from entities.team import *
import datetime 

app = Flask(__name__)
app.secret_key = '+_9o$w9+9xro!-y(wvuv+vvyc!$x(@ak(!oh@ih0ul+6cf=$f'


def date2str(o):
    if isinstance(o, datetime.date):
        return o.__str__()


def str2date(o):
    return datetime.datetime.strptime(o, '%Y-%m-%d').date()


@app.route('/api/teams', methods=['GET', 'POST'])
def teams_page():
    if request.method == "POST":
        data = request.data.decode()
        data = json.loads(data)
        team_id = data['id']
        team_name = data['name']

        added_team = Team(1, team_name)
        try:
            connection = dbconnector.connect("dbname='taskerdb' user='tasker' host='localhost' password='tasker'")
            cursor = connection.cursor()
            create_team(cursor, added_team)
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
            teams_list = get_all_teams(cursor)
        except dbconnector.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
            return json.dumps([list(elem) for elem in teams_list], default=date2str)


@app.route('/api/teams/<string:teamId>', methods=['GET', 'POST'])
def team_details(teamId):
    if request.method == "POST":
        data = request.data.decode()
        data = json.loads(data)
        user_id = data['userId']

        try:
            connection = dbconnector.connect("dbname='taskerdb' user='tasker' host='localhost' password='tasker'")
            cursor = connection.cursor()
            add_user_to_team(cursor, teamId, user_id)
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
            team = get_team_members(cursor, teamId)
        except dbconnector.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
            return json.dumps(list(team), default=date2str)


@app.route('/api/removeteammember/id=<string:relation_id>', methods=['POST', 'GET'])
def remove_member_from_team(relation_id):
    try:
        connection = dbconnector.connect("dbname='taskerdb' user='tasker' host='localhost' password='tasker'")
        cursor = connection.cursor()
        delete_user_from_team(cursor, relation_id)
    except dbconnector.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.commit()
        connection.close()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)
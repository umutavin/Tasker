from entities.user import *
from flask import Flask,  g, jsonify
import psycopg2 as dbconnector
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
app.secret_key = '+_9o$w9+9xro!-y(wvuv+vvyc!$x(@ak(!oh@ih0ul+6cf=$f'

auth = HTTPBasicAuth()


def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None
    except BadSignature:
        return None
    return data['id']


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(app, 600)
    return jsonify({ 'token': token.decode('ascii') })


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


@app.route('/api/get_username')
@auth.login_required
def get_username():
    return jsonify({'username': g.user.username, 'id':g.user.id})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=False)

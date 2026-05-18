#!/usr/bin/env python3
import base64
import os
import threading
from datetime import datetime

import pymysql
from flask import Flask, abort, redirect, render_template, request, session

import admin_bot

ROLE_USER = 0
ROLE_ADMIN = 1

with open('./flag', 'r') as f:
    FLAG = f.read()

app = Flask(__name__)
app.secret_key = os.urandom(32)

def connect_mysql():
    db = pymysql.connect(host='localhost',
                         port=3306,
                         user=os.environ['MYSQL_USER'],
                         passwd=os.environ['MYSQL_PASSWORD'],
                         db='dream_lectures_db',
                         charset='utf8')
    cursor = db.cursor()
    return db, cursor

def get_seed():
    seed = 0
    while seed == 0:
        seed = int.from_bytes(os.urandom(2), byteorder='little')
    return seed

def get_rand32bits():
    global seed

    rand32bits = 0

    for i in range(32):
        rand32bits |= (seed & 1) << i
        feedback = seed & 1 ^ seed >> 2 & 1 ^ seed >> 3 & 1 ^ seed >> 5 & 1
        seed = (seed >> 1) | feedback << 15
    return rand32bits

def get_nonce():
    nonce = 0

    for i in range(4):
        randn = get_rand32bits()
        nonce |= randn << i * 32
    nonce ^= 0xbeefbeefcafecafe13371337defaced0
    return nonce

def reset_admin_password():
    global admin_pw

    admin_pw = base64.b64encode(os.urandom(32))

    db, cursor = connect_mysql()
    try:
        query = 'UPDATE users SET upw = %s WHERE uid = \'admin\''
        cursor.execute(query, (admin_pw, ))
        db.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()

seed = get_seed()
nonce = hex(get_nonce())[2:]
admin_pw = None

@app.after_request
def add_header(response):
    global nonce

    csp = f"default-src 'self'; " \
          f"script-src 'self' 'nonce-{nonce}' 'unsafe-inline'; " \
          f"img-src 'self'; " \
          f"style-src 'self'; " \
          f"object-src 'none'; " \
          f"base-uri 'none';"
    response.headers['Content-Security-Policy'] = csp
    nonce = hex(get_nonce())[2:]
    return response

@app.route('/', methods=['GET'])
def index():
    return redirect('/lectures') if session else redirect('/sign_in')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if session:
        return redirect('/lectures')

    if request.method == 'GET':
        return render_template('login.html')

    # POST
    args = request.form

    if 'username' not in args or 'password' not in args:
        return render_template('login.html',
                msg='Enter username and password.')

    username = args['username']
    password = args['password']

    db, cursor = connect_mysql()
    try:
        query = 'SELECT * FROM users WHERE uid = %s and upw = %s'
        cursor.execute(query, (username, password, ))
        ret = cursor.fetchone()
    except Exception as e:
        print(e)
        return render_template('login.html', msg='something went wrong!')
    finally:
        cursor.close()
        db.close()

    if not ret:
        return render_template('login.html',
                msg='Username or password is wrong.')

    session['username'] = username
    session['role'] = ret[3]

    return redirect('/lectures')

@app.route('/sign_up', methods=['POST'])
def sign_up():
    if session:
        return redirect('/lectures')

    args = request.form

    if 'username' not in args or 'password' not in args:
        return render_template('login.html',
                msg='Enter username and password.')

    username = args['username']
    password = args['password']

    db, cursor = connect_mysql()
    try:
        query = 'INSERT INTO users (uid, upw, role) VALUES (%s, %s, %s)'
        cursor.execute(query, (username, password, ROLE_USER))
        db.commit()
    except Exception as e:
        print(e)
        return render_template('login.html', msg='Failed to sign up!')
    finally:
        cursor.close()
        db.close()

    return render_template('login.html', msg='Signed up successfully!')

@app.route('/logout', methods=['POST'])
def logout():
    if session:
        session.clear()

    return redirect('/sign_in')

@app.route('/lectures', methods=['GET'])
def lectures():
    if not session:
        return redirect('/sign_in')

    db, cursor = connect_mysql()
    try:
        query = 'SELECT idx, lecture_name FROM lectures'
        cursor.execute(query)
        ret = cursor.fetchall()
    except Exception as e:
        print(e)
        abort(400)
    finally:
        cursor.close()
        db.close()

    return render_template('lectures.html', lectures=ret)

@app.route('/lectures/<lecture_id>', methods=['GET'])
def lectures_lecture(lecture_id):
    if not session:
        return redirect('/sign_in')

    if not lecture_id.isdigit():
        abort(400, description='lecture_id must be a number.')

    db, cursor = connect_mysql()
    try:
        query = 'SELECT lecture_name, lecturer_name, description, ' \
                'registration_start, registration_due, lecture_start, ' \
                'lecture_end FROM lectures WHERE idx = %s'
        cursor.execute(query, (lecture_id, ))
        ret = cursor.fetchone()
    except Exception as e:
        print(e)
        abort(400)
    finally:
        cursor.close()
        db.close()

    if not ret:
        abort(404)

    lecture_name = ret[0]
    lecturer_name = ret[1]
    description = ret[2]
    registration_start = ret[3]
    registration_due = ret[4]
    lecture_start = ret[5]
    lecture_end = ret[6]

    if datetime.now() < registration_start \
            or registration_due < datetime.now():
        return render_template('lecture_application.html',
                lecture_id=lecture_id,
                lecture_name=lecture_name,
                lecturer_name=lecturer_name,
                description=description,
                lecture_start=lecture_start,
                lecture_end=lecture_end,
                registration_start=registration_start,
                registration_due=registration_due,
                is_ended=True)

    return render_template('lecture_application.html',
            lecture_id=lecture_id,
            lecture_name=lecture_name,
            lecturer_name=lecturer_name,
            description=description,
            lecture_start=lecture_start,
            lecture_end=lecture_end,
            registration_start=registration_start,
            registration_due=registration_due)

@app.route('/apply_lecture', methods=['POST'])
def apply_lecture():
    if not session:
        return redirect('/sign_in')

    args = request.form

    if 'lecture_id' not in args or not args['lecture_id']:
        abort(404, description='lecture_id is not given.')

    lecture_id = args['lecture_id']

    if not lecture_id.isdigit():
        abort(400, description='lecture_id must be a number.')

    if 'applicant_name' not in args or not args['applicant_name']:
        abort(400, description='applicant_name is not given.')

    applicant_name = args['applicant_name']

    if 'email' not in args or not args['email']:
        abort(400, description='email is not given.')

    email = args['email']

    if '@' not in email:
        abort(400, description='email must contain \'@\'.')

    if 'contact' not in args or not args['contact']:
        abort(400, description='contact is not given.')

    contact = args['contact']

    if '-' not in contact:
        abort(400, description='contact must contain \'-\'.')

    if 'reason' not in args or not args['reason']:
        abort(400, description='reason is not given.')

    reason = args['reason']

    if not lecture_id.isdigit():
        abort(400, description="lecture_id must be a number.")

    db, cursor = connect_mysql()
    try:
        query = 'SELECT lecture_name, lecturer_name, description, ' \
                'registration_start, registration_due, lecture_start, ' \
                'lecture_end FROM lectures WHERE idx = %s'
        cursor.execute(query, (lecture_id, ))
        ret = cursor.fetchone()
    except Exception as e:
        print(e)
        abort(400)
    finally:
        cursor.close()
        db.close()

    if not ret:
        abort(404)

    lecture_name = ret[0]
    lecturer_name = ret[1]
    description = ret[2]
    registration_start = ret[3]
    registration_due = ret[4]
    lecture_start = ret[5]
    lecture_end = ret[6]

    db, cursor = connect_mysql()
    try:
        query = 'SELECT lecture_name FROM lectures WHERE idx = %s'
        cursor.execute(query, (lecture_id))
        ret = cursor.fetchone()
    except Exception as e:
        print(e)
        abort(400, description='something went wrong!')
    finally:
        cursor.close()
        db.close()

    if not ret:
        abort(400, description='could not get lecture_name.')

    lecture_name = ret[0]

    db, cursor = connect_mysql()
    try:
        query = 'INSERT INTO applications (' \
                'lecture_idx, lecture_name, applicant_name, email, ' \
                'contact, reason, is_checked) VALUES (' \
                '%s, %s, %s, %s, ' \
                '%s, %s, false)'
        cursor.execute(query, (lecture_id, lecture_name, applicant_name,
                email, contact, reason))
        db.commit()
    except Exception as e:
        print(e)
        abort(400)
    finally:
        cursor.close()
        db.close()

    admin_bot.read_applications()

    return render_template('lecture_application.html',
            lecture_id=lecture_id,
            lecture_name=lecture_name,
            lecturer_name=lecturer_name,
            description=description,
            lecture_start=lecture_start,
            lecture_end=lecture_end,
            registration_start=registration_start,
            registration_due=registration_due,
            is_ended = True,
            msg='lecture applied successfully!')


@app.route('/create_lecture', methods=['GET', 'POST'])
def create_lecture():
    if not session or (session and session['role'] != ROLE_ADMIN):
        abort(404)

    if request.method == 'GET':
        return render_template('create_lecture.html')

    # POST
    args = request.form

    if 'lecture_name' not in args:
        return render_template('create_lecture.html',
                msg='lecture name is not given.')

    if 'lecturer_name' not in args:
        return render_template('create_lecture.html',
                msg='lecturer name is not given.')

    if 'description' not in args:
        return render_template('create_lecture.html',
                msg='description is not given.')

    if 'registration_start' not in args:
        return render_template('create_lecture.html',
                msg='registration start datetime is not given.')

    try:
        datetime.strptime(args['registration_start'],
                '%Y-%m-%d %H:%M:%S').timestamp()
    except:
        return render_template('create_lecture.html',
                msg='Registration Start Datetime must be YYYY-mm-dd HH:MM:SS.')

    if 'registration_due' not in args:
        return render_template('create_lecture.html',
                msg='registration due datetime is not given.')

    try:
        datetime.strptime(args['registration_due'],
                '%Y-%m-%d %H:%M:%S').timestamp()
    except:
        return render_template('create_lecture.html',
                msg='Registration Due Datetime must be YYYY-mm-dd HH:MM:SS.')

    if 'lecture_start' not in args:
        return render_template('create_lecture.html',
                msg='lecture start datetime is not given.')

    try:
        datetime.strptime(args['lecture_start'],
                '%Y-%m-%d %H:%M:%S').timestamp()
    except:
        return render_template('create_lecture.html',
                msg='Lecture Start Datetime must be YYYY-mm-dd HH:MM:SS.')

    if 'lecture_end' not in args:
        return render_template('create_lecture.html',
                msg='lecture end datetime is not given.')

    try:
        datetime.strptime(args['lecture_end'], '%Y-%m-%d %H:%M:%S').timestamp()
    except:
        return render_template('create_lecture.html',
                msg='Lecture End Datetime must be YYYY-mm-dd HH:MM:SS.')

    db, cursor = connect_mysql()
    try:
        query = 'INSERT INTO lectures (' \
                'lecture_name, lecturer_name, description, ' \
                'registration_start, registration_due, lecture_start, ' \
                'lecture_end) VALUES (' \
                '%s, %s, %s, ' \
                '%s, %s, %s, ' \
                '%s)'
        cursor.execute(query, (args['lecture_name'], args['lecturer_name'],
                args['description'], args['registration_start'],
                args['registration_due'], args['lecture_start'],
                args['lecture_end'], ))
        db.commit()
    except Exception as e:
        print(e)
        return render_template('create_lecture.html',
                msg='something went wrong!')
    finally:
        cursor.close()
        db.close()

    return redirect('/lectures')

@app.route('/applications', methods=['GET'])
def applications():
    if not session or (session and session['role'] != ROLE_ADMIN):
        abort(404)

    db, cursor = connect_mysql()
    try:
        query = 'SELECT idx, lecture_idx, lecture_name, applicant_name ' \
                'FROM applications WHERE is_checked = false'
        cursor.execute(query)
        ret = cursor.fetchall()
    except Exception as e:
        print(e)
        abort(400)
    finally:
        cursor.close()
        db.close()

    if not ret:
        abort(404)

    return render_template('applications.html', applications=ret)

@app.route('/applications/<application_id>', methods=['GET'])
def applications_application(application_id):
    if not session or (session and session['role'] != ROLE_ADMIN):
        abort(404)

    if not application_id.isdigit():
        abort(400, description='application_id must be a number.')

    db, cursor = connect_mysql()
    try:
        query = 'SELECT lecture_idx, lecture_name, applicant_name, '\
                'email, contact, reason FROM applications WHERE idx = %s'
        cursor.execute(query, (application_id, ))
        ret = cursor.fetchone()
    except Exception as e:
        print(e)
        abort(400)
    finally:
        cursor.close()
        db.close()

    if not ret:
        abort(404)

    lecture_idx = ret[0]
    lecture_name = ret[1]
    applicant_name = ret[2]
    email = ret[3]
    contact = ret[4]
    reason = ret[5]

    db, cursor = connect_mysql()
    try:
        query = 'SELECT lecture_name, lecturer_name, description, ' \
                'lecture_start, lecture_end, registration_start, ' \
                'registration_due FROM lectures WHERE idx = %s'
        cursor.execute(query, (lecture_idx, ))
        ret = cursor.fetchone()
    except Exception as e:
        print(e)
        abort(400)
    finally:
        cursor.close()
        db.close()

    if not ret:
        abort(404)

    lecture_name = ret[0]
    lecturer_name = ret[1]
    description = ret[2]
    lecture_start = ret[3]
    lecture_end = ret[4]
    registration_start = ret[5]
    registration_due = ret[6]

    db, cursor = connect_mysql()
    try:
        query = 'UPDATE applications SET is_checked = true WHERE idx = %s'
        cursor.execute(query, (application_id, ))
        db.commit()
    except Exception as e:
        print(e)
        abort(400)
    finally:
        cursor.close()
        db.close()

    return render_template('applications_application.html',
            lecture_name=lecture_name,
            lecturer_name=lecturer_name,
            description=description,
            lecture_start=lecture_start,
            lecture_end=lecture_end,
            registration_start=registration_start,
            registration_due=registration_due,
            applicant_name=applicant_name,
            email=email,
            contact=contact,
            reason=reason)

@app.route('/admin', methods=['GET'])
def admin_page():
    if not session or (session and session['role'] != ROLE_ADMIN):
        abort(404)

    return FLAG

if __name__ == '__main__':
    reset_admin_password()
    thd = threading.Thread(target=admin_bot.login, args=(admin_pw, ))
    thd.start()
    app.config.update(SESSION_COOKIE_HTTPONLY=False)
    app.run(host='0.0.0.0', port=8000)

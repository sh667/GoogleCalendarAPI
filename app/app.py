
from flask_email_verifier import EmailVerifier
from json import dumps, loads
from flask import *
from flask_mail import *
from random import *
from itsdangerous import URLSafeTimedSerializer
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime
import googleapiclient


app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root' #os.environ['MYSQL_ROOT_PASSWORD']
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'final_project_db'
mysql.init_app(app)
# Initialize the extension
app.config['EMAIL_VERIFIER_KEY'] = 'at_d2rnczuTQlRMWTq5qElyv5fr4nwYi'
verifier = EmailVerifier(app)

mail_settings = {
    "MAIL_SERVER" : 'smtp.gmail.com',
    "MAIL_PORT" : 465,
    "MAIL_USERNAME" : 'nt27gradprojects@gmail.com',
    "MAIL_PASSWORD" : 'Project@2020',
    "MAIL_USE_TLS" : False,
    "MAIL_USE_SSL" : True
}
app.config.update(mail_settings)
mail = Mail(app)

otp = randint(000000,999999)

app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'credentials.json'


@app.route('/', methods=['GET'])
def index() -> str:
    return render_template('login.html', title='Login')


@app.route('/login', methods=['POST'])
def login_submit() -> str:
    cursor = mysql.get_db().cursor()
    email = request.form.get('login_name')
    password = request.form.get('password')
    input_data = (email, password)
    login_query = """SELECT * FROM app_users where email = %s and password = %s """
    cursor.execute(login_query, input_data)
    result = cursor.fetchone()
    if result is not None and len(result) > 0:
        # message = { 'message': 'Success - Welcome!'+result['first_name']+' '+result['last_name'] }
        return get_all_events()
    else:
        message = {'message': 'Error - Username/Password incorrect!'}
        return render_template('login.html', message=message, title='Login')


@app.route('/signup', methods=['GET'])
def form_sign_up():
    return render_template('signup.html', title='Sign Up')


@app.route('/signup', methods=['POST'])
def sign_up_submit() -> str:
    cursor = mysql.get_db().cursor()
    email = request.form.get('email_id')
    input_data = (request.form.get('first_name'), request.form.get('last_name')
                    , email, request.form.get('password')
                    , request.form.get('phone'))
    sign_up_query = """INSERT INTO app_users (first_name,last_name,email,password,phone,status_id,confirmed,created_on) 
                            VALUES ( %s, %s, %s, %s, %s, 1, 0, CURRENT_TIMESTAMP) """
    cursor.execute(sign_up_query, input_data)
    mysql.get_db().commit()
    # added to verify email address
    return verify(email)


@app.route('/edit-user', methods=['GET'])
def edit_user() -> str:
    return render_template("edit_profile.html", user="")

@app.route('/update-user/<email_id>', methods=['POST'])
def update_user() -> str:
    cursor = mysql.get_db().cursor()
    email = request.form.get('email_id')
    input_data = (request.form.get('first_name'), request.form.get('last_name'), request.form.get('phone'))
    sign_up_query = """UPDATE app_users set first_name=%s,last_name=s%, phone=%s, updated_on=CURRENT_TIMESTAMP where  """
    cursor.execute(sign_up_query, input_data)
    mysql.get_db().commit()
    # added to verify email address
    message = {'message': 'Profile updated successfully!'}
    return render_template("edit_profile.html", message=message, user="")


def verify(email):
    msg = Message(subject="Hello",
                  sender=app.config.get("MAIL_USERNAME"),
                  recipients=[email],  # replace with your email for testing
                  body=str(otp)
                  )
    mail.send(msg)
    return render_template('verify.html')


@app.route('/verify-email',methods=["POST"])
def validate():
    user_otp = request.form['otp']
    if otp == int(user_otp):
        # sign_up_query = 'UPDATE app_users set confirmed=1, confirmed_on=CURRENT_TIMESTAMP'
        # cursor = mysql.get_db().cursor()
        # cursor.execute(sign_up_query)
        # mysql.get_db().commit()
        message = {'message': 'Email Verified successfully. Sign Up is now complete. You may now login.'}
        return render_template("login.html", message=message)
    else:
        message = {'message': 'Incorrect OTP, Please retry!'}
        return render_template("verify.html", message=message)


@app.route('/validate-email/<email>')
def email(email):
    # Retrieve an info for the given email address
    email_address_info = verifier.verify(email)
    if email_address_info is not None:
        data = dumps(loads(email_address_info.json_string), indent=4)
        resp = make_response(data, 200)
        resp.headers['Content-Type'] = 'application/json'
    else:
        resp = make_response('None', 404)

    return resp


@app.route('/reset-password', methods=['GET'])
def reset_password_form():
    return render_template('reset_password.html', title='Reset Password')


@app.route('/reset-password', methods=['POST'])
def reset_password_submit() -> str:
    cursor = mysql.get_db().cursor()
    #content = request.json
    inputData = (request.form.get('login_name'), request.form.get('password'))
    login_query = """SELECT count(1) FROM app_users where email = %s and password = %s """
    cursor.execute(login_query, inputData)
    result = cursor.fetchall()
    json_result = json.dumps(result)
    if int(json_result) > int(0):

        return render_template('index.html', title='Home')
    else:
        return render_template('login.html', title='Login')

@app.route('/event', methods=['GET'])
def get_all_events():
    user = {'username': 'Calendar Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM events')
    result = cursor.fetchall()
    return render_template('events_list.html', title='Home', user=user, event_name=result)


@app.route('/view/<int:event_id>', methods=['GET'])
def record_view(event_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM events WHERE id=%s', event_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', event=result[0])


@app.route('/edit/<int:event_id>', methods=['GET'])
def form_edit_get(event_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM events WHERE id=%s', event_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', event=result[0])


@app.route('/edit/<int:event_id>', methods=['POST'])
def form_update_post(event_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('title'), request.form.get('start_event'), request.form.get('end_event'), event_id)
    sql_update_query = """UPDATE events t SET t.title = %s, t.start_event = %s, t.end_event = %s
     WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    cursor.execute('SELECT * FROM events WHERE id=%s', event_id)
    result = cursor.fetchall()
    a = result[0]
    titlenew = a['title']
    startnew = str(a['start_event'])
    startnew = startnew.replace(" ", "T")
    endnew = str(a['end_event'])
    endnew = endnew.replace(" ", "T")
    key=str(a['event_id'])
    update_event(titlenew,startnew,endnew,key)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/event_name/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Event Form')


@app.route('/event_name/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('title'), request.form.get('start_event'), request.form.get('end_event'))
    sql_insert_query = """INSERT INTO events (title,start_event,end_event) VALUES (%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    print(sql_insert_query)
    cursor.execute("select title,start_event,end_event from events where id = (select max(id) from events)")
    row_data = cursor.fetchall()
    a = row_data[0]
    titlenew = a['title']
    startnew = str(a['start_event'])
    startnew = startnew.replace(" ", "T")
    endnew = str(a['end_event'])
    endnew = endnew.replace(" ", "T")
    id_cal = create_event(startnew, endnew, titlenew)

    cursor.execute("select max(id) from events")
    col_data = cursor.fetchall()
    col = col_data[0]
    col_new = col['max(id)']
    cursor.execute("UPDATE events SET event_id=%s WHERE id=%s", (id_cal, col_new))

    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:event_id>', methods=['POST'])
def form_delete_post(event_id):
    key=event_id
    cursor = mysql.get_db().cursor()
    cursor.execute("select event_id from events where id=%s",(key))
    key_value= cursor.fetchall()
    key_old = key_value[0]
    key_new = key_old['event_id']
    delete_event(key_new)
    sql_delete_query = """DELETE FROM events WHERE id = %s """
    cursor.execute(sql_delete_query, event_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/event_name', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM events')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/event_name/<int:event_id>', methods=['GET'])
def api_retrieve(event_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM events WHERE id=%s', event_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/event_name/<int:event_id>', methods=['PUT'])
def api_edit(event_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['title'], content['start_event'], content['end_event'],
                 event_id)
    sql_update_query = """UPDATE events t SET t.title = %s, t.start_event = %s, t.end_event = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/event_name', methods=['POST'])
def api_add() -> str:
    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['title'], content['start_event'], content['end_event'])
    sql_insert_query = """INSERT INTO events (title,start_event,end_event) VALUES (%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/event_name/<int:event_id>', methods=['DELETE'])
def api_delete(event_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM events WHERE id = %s """
    cursor.execute(sql_delete_query, event_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


def get_calendar_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


def create_event(start, end, a):
    service = get_calendar_service()
    event_result = service.events().insert(calendarId='primary',
                                           body={
                                               "summary": a,
                                               "start": {"dateTime": start, "timeZone": 'America/New_York'},
                                               "end": {"dateTime": end, "timeZone": 'America/New_York'},
                                           }
                                           ).execute()
    return event_result['id']


def update_event(a,start, end,key):
    # update the event to tomorrow 9 AM IST
    service = get_calendar_service()
    start = start
    end = end
    task = a
    event_result = service.events().update(
        calendarId='primary',
        eventId=key,
        body={
            "summary": task,
            "start": {"dateTime": start, "timeZone": 'America/New_York'},
            "end": {"dateTime": end, "timeZone": 'America/New_York'},
        },
    ).execute()
    print("updated event")
    print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    print("starts at: ", event_result['start']['dateTime'])
    print("ends at: ", event_result['end']['dateTime'])


def delete_event(value):
    # Delete the event
    print(value)
    service = get_calendar_service()
    try:
        service.events().delete(
            calendarId='primary',
            eventId=value,
        ).execute()
    except googleapiclient.errors.HttpError:
        print("Failed to delete event")

    print("Event deleted")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
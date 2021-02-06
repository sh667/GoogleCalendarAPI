from typing import List, Dict
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
from datetime import datetime, timedelta
import googleapiclient


app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'final_project_db'
mysql.init_app(app)

# from cal_setup import get_calendar_service
# If modifying these scopes, delete the file token.pickle.


SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'credentials.json'


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


@app.route('/event', methods=['GET'])
def get_all_events():
    user = {'username': 'Calendar Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM events')
    result = cursor.fetchall()
    return render_template('event_list.html', title='Home', user=user, event_name=result)


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

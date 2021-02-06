from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'final_project_db'
mysql.init_app(app)


@app.route('/api/v1/users', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute("""SELECT * FROM app_users where status_id = 1 order by id desc""")
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/user/<int:id>', methods=['GET'])
def api_retrieve(id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute("""SELECT * FROM app_users WHERE id=%s""", id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/user', methods=['POST'])
def api_add() -> str:
    content = request.json
    cursor = mysql.get_db().cursor()
    inputData = (content['login_name'], content['password'], content['first_name'], content['last_name']
                 , content['role_id'], content['type_id'], content['status_id'], content['address_id'])
    sql_insert_query = """INSERT INTO app_users 
                        (login_name,password,first_name,last_name,role_id,type_id,status_id,address_id) 
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/user/<int:id>', methods=['PUT'])
def api_edit(id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['login_name'], content['password'], content['first_name'], content['last_name']
                 , content['role_id'], content['type_id'], content['status_id'], content['address_id']
                 , id)
    sql_update_query = """UPDATE app_users t 
                                SET t.login_name = %s, t.password = %s, t.first_name = %s, t.last_name = %s
                                , t.role_id = %s, t.type_id = %s, t.status_id = %s, t.address_id = %s
                                WHERE t.Id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/user/<int:id>', methods=['DELETE'])
def api_delete(id) -> str:
    cursor = mysql.get_db().cursor()
    sql_update_query = """UPDATE app_users au
                            SET au.status_id= %s 
                            WHERE au.id = %s """
    cursor.execute(sql_update_query, 2, id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/login', methods=['POST'])
def api_login() -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['login_name'], content['password'])
    login_query = """SELECT count(1) FROM app_users where login_name = %s and password = %s """
    cursor.execute(login_query, inputData)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    if int(json_result) > int(0):
        j_r = json.dumps('true')
    else:
        j_r = json.dumps('false')

    resp = Response(j_r, status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
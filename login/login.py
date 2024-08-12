import mysql.connector
from flask import jsonify, request
from dbconfig import db_config

def execute_select_query(query, params=None):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    finally:
        cursor.close()
        connection.close()

def login_data():
    try:
        data = request.get_json()
        username = data.get('username').strip()
        password = data.get('password').strip()
        select_query = "SELECT * FROM `users` WHERE `username` = %s AND `password` = %s"
        result = execute_select_query(select_query, (username, password))
        if len(result) == 1:
            for row in result:
                flag=row['flag']
                return jsonify({"success": 1,"flag":flag}), 200
        else:
            select_pquery = "SELECT * FROM `users` WHERE `username` = %s AND `password` <> %s"
            presult = execute_select_query(select_pquery, (username, password))
            if len(presult) == 1:
                return jsonify({"success": 2}), 200
            else:
                return jsonify({"success": 3}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

import mysql.connector
from flask import jsonify, request
from dbconfig import db_config

def execute_select_query(query):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    finally:
        cursor.close()
        connection.close()
def transporter_get_data():
    select_query = "SELECT * FROM transporter"
    
    try:
        result = execute_select_query(select_query)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})
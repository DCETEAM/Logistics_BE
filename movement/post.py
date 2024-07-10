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


def movement_post_data():
    request_data = request.json
    bill_number = request_data.get('billNumber')
    if bill_number:
        select_query = f"SELECT * FROM movement WHERE billNumber = '{bill_number}'"
    else:
        return jsonify({'error': 'Bill number is required in the request body.'}), 400
    
    try:
        result = execute_select_query(select_query)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
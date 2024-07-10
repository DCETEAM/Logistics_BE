import mysql.connector
from flask import jsonify, request
from dbconfig import db_config

def execute_select_query(query, data=None):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query, data)
        result = cursor.fetchall()
        return result
    finally:
        cursor.close()
        connection.close()

def truck_search_data():
    try:
        search_query = request.args.get('query')
        select_query = "SELECT * FROM truck WHERE "
        columns = ["truckNumber", "registrationDate", "chassisNumber", "insuranceExpiryDate", "taxExpiryDate", "fcExpiryDate",
                   "LPEXD", "NPEXD"]
        
        conditions = " OR ".join([f"{column} LIKE %s" for column in columns])
        select_query += conditions
        search_query_like = f"%{search_query}%"
        data = tuple([search_query_like] * len(columns))

        result = execute_select_query(select_query, data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

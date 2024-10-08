import mysql.connector
from flask import jsonify, request
from dbconfig import db_config

def execute_insert_query(query, data):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        result = cursor.execute(query, data)
        connection.commit()
        return result
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()

def accounts_insert_data():
    try:
        data = request.get_json()
        print("Received data:", data) 
        
        insert_query = "INSERT INTO `accounts` (`referenceName`, `bankName`, `accountNumber`, `accountHolderName`, `ifscCode`, `panNumber`) VALUES (%s, %s, %s, %s, %s, %s)"
        accounts_insert_data = (
            data['referenceName'],
            data['bankName'],
            data['accountNumber'],
            data['accountHolderName'],
            data['ifscCode'],
            data['panNumber']


        )
        result = execute_insert_query(insert_query, accounts_insert_data)
        return jsonify({'message': "Insert Success."})
    except Exception as e:
        print("Error inserting data:", e) 
        return jsonify({'error': str(e)})

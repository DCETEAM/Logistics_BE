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

def transporter_insert_data():
    try:
        data = request.get_json()
        print("Received data:", data) 
        
        insert_query = "INSERT INTO `transporter` (`name`, `mobileNumber`, `dateOfJoining`, `location`, `bankName`, `accountNumber`, `accountHolderName`, `ifscCode`, `panNumber`, `address`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        transporter_insert_data = (
            data['name'],
            data['mobileNumber'],
            data['dateOfJoining'],
            data['location'], 
            data['bankName'], 
            data['accountNumber'],
            data['accountHolderName'],
            data['ifscCode'],
            data['panNumber'],
            data['address']
        )
        result = execute_insert_query(insert_query, transporter_insert_data)
        return jsonify({'message': "Insert Success."})
    except Exception as e:
        print("Error inserting data:", e) 
        return jsonify({'error': str(e)})

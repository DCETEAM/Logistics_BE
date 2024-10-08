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

def driver_insert_data():
    try:
        data = request.get_json()
        print("Received data:", data) 
        
        insert_query = "INSERT INTO `driver` (`name`, `mobileNumber`, `mobileNo`, `phoneNo`, `dateOfBirth`,`licenseNumber`, `licenseIssueDate`, `licenseExpiryDate`, `dateOfJoining`, `branch`, `referredBy`, `accountNumber`, `accountHolderName`, `ifscCode`, `address`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        driver_insert_data = (
            data['name'],
            data['mobileNumber'],
            data['mobileNo'], 
            data['phoneNo'], 
            data['dateOfBirth'],
            data['licenseNumber'],  
            data['licenseIssueDate'],
            data['licenseExpiryDate'],
            data['dateOfJoining'],
            data['branch'],
            data['referredBy'],
            data['accountNumber'],
            data['accountHolderName'],
            data['ifscCode'],
            data['address']
        )
        result = execute_insert_query(insert_query, driver_insert_data)
        return jsonify({'message': "Insert Success."})
    except Exception as e:
        print("Error inserting data:", e) 
        return jsonify({'error': str(e)})

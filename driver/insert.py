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
            data['name'].strip(),
            data['mobileNumber'].strip(),
            data['mobileNo'].strip(), 
            data['phoneNo'].strip(), 
            data['dateOfBirth'].strip(),
            data['licenseNumber'].strip(),  
            data['licenseIssueDate'].strip(),
            data['licenseExpiryDate'].strip(),
            data['dateOfJoining'].strip(),
            data['branch'].strip(),
            data['referredBy'].strip(),
            data['accountNumber'].strip(),
            data['accountHolderName'].strip(),
            data['ifscCode'].strip(),
            data['address'].strip()
        )
        result = execute_insert_query(insert_query, driver_insert_data)
        return jsonify({'message': "Insert Success."})
    except Exception as e:
        print("Error inserting data:", e) 
        return jsonify({'error': str(e)})

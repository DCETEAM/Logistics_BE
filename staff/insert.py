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

def staff_insert_data():
    try:
        data = request.get_json()
        print("Received data:", data) 
        
        insert_query = "INSERT INTO `staff` (`name`, `mobileNumber`, `mobileNo`, `dateOfJoining`,`username`, `password`, `accountNumber`, `accountHolderName`, `ifscCode`, `address`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        staff_insert_data = (
            data['name'].strip(),
            data['mobileNumber'].strip(),
            data['mobileNo'].strip(),                  
            data['dateOfJoining'].strip(),
            data['username'].strip(),
            data['password'].strip(),
            data['accountNumber'].strip(),
            data['accountHolderName'].strip(),
            data['ifscCode'].strip(),
            data['address'].strip()
        )

        insert_staff = "INSERT INTO `users`(`username`, `password`) VALUES (%s,%s)"
        staff_user_data = (   
            data['username'].strip(),
            data['password'].strip(),
        )


        result = execute_insert_query(insert_query, staff_insert_data)

        result1 = execute_insert_query(insert_staff, staff_user_data)


        return jsonify({'message': "Insert Success."})
    except Exception as e:
        print("Error inserting data:", e) 
        return jsonify({'error': str(e)})

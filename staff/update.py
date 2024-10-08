import mysql.connector
from flask import jsonify, request
from dbconfig import db_config

def execute_update_query(query, data):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        cursor.execute(query, data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()
def staff_update_data():
    try:
        data = request.get_json()
        update_query = "UPDATE staff SET "
        update_fields = []

        if 'mobileNumber' in data:
            update_query += "mobileNumber = %s, "
            update_fields.append(data['mobileNumber'].strip())

        if 'name' in data:
            update_query += "name = %s, "
            update_fields.append(data['name'].strip())

        if 'accountNumber' in data:
            update_query += "accountNumber = %s, "
            update_fields.append(data['accountNumber'].strip())

        if 'dateOfJoining' in data:
            update_query += "dateOfJoining = %s, "
            update_fields.append(data['dateOfJoining'].strip())

        if 'mobileNo' in data:
            update_query += "mobileNo = %s, "
            update_fields.append(data['mobileNo'].strip())

        if 'username' in data:
            update_query += "username = %s, "
            update_fields.append(data['username'].strip())

        if 'password' in data:
            update_query += "password = %s, "
            update_fields.append(data['password'].strip())

        if 'accountHolderName' in data:
            update_query += "accountHolderName = %s, "
            update_fields.append(data['accountHolderName'].strip())

        if 'ifscCode' in data:
            update_query += "ifscCode = %s, "
            update_fields.append(data['ifscCode'].strip())

        if 'address' in data:
            update_query += "address = %s, "
            update_fields.append(data['address'].strip())
            
        update_query = update_query.rstrip(', ') + " WHERE id = %s"

        update_fields.append(data['id'])

        execute_update_query(update_query, tuple(update_fields))
        return jsonify({'message': 'Data updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
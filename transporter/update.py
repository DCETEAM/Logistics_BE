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
def transporter_update_data():
    try:
        data = request.get_json()
        update_query = "UPDATE transporter SET "
        update_fields = []

        if 'mobileNumber' in data:
            update_query += "mobileNumber = %s, "
            update_fields.append(data['mobileNumber'])

        if 'name' in data:
            update_query += "name = %s, "
            update_fields.append(data['name'])

        if 'accountNumber' in data:
            update_query += "accountNumber = %s, "
            update_fields.append(data['accountNumber'])

        if 'location' in data:
            update_query += "location = %s, "
            update_fields.append(data['location'])

        if 'accountHolderName' in data:
            update_query += "accountHolderName = %s, "
            update_fields.append(data['accountHolderName'])

        if 'ifscCode' in data:
            update_query += "ifscCode = %s, "
            update_fields.append(data['ifscCode'])

        if 'bankName' in data:
            update_query += "bankName = %s, "
            update_fields.append(data['bankName'])

        if 'panNumber' in data:
            update_query += "panNumber = %s, "
            update_fields.append(data['panNumber'])

        if 'address' in data:
            update_query += "address = %s, "
            update_fields.append(data['address'])

        if 'dateOfJoining' in data:
            update_query += "dateOfJoining = %s, "
            update_fields.append(data['dateOfJoining'])        
            
        update_query = update_query.rstrip(', ') + " WHERE id = %s"

        update_fields.append(data['id'])

        execute_update_query(update_query, tuple(update_fields))
        return jsonify({'message': 'Data updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
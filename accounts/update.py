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
def accounts_update_data():
    try:
        data = request.get_json()
        update_query = "UPDATE accounts SET "
        update_fields = []

        if 'accountNumber' in data:
            update_query += "accountNumber = %s, "
            update_fields.append(data['accountNumber'].strip())

        if 'referenceName' in data:
            update_query += "referenceName = %s, "
            update_fields.append(data['referenceName'].strip())

        if 'accountHolderName' in data:
            update_query += "accountHolderName = %s, "
            update_fields.append(data['accountHolderName'].strip())

        if 'ifscCode' in data:
            update_query += "ifscCode = %s, "
            update_fields.append(data['ifscCode'].strip())

        if 'bankName' in data:
            update_query += "bankName = %s, "
            update_fields.append(data['bankName'].strip())

        if 'panNumber' in data:
            update_query += "panNumber = %s, "
            update_fields.append(data['panNumber'].strip())

            
        update_query = update_query.rstrip(', ') + " WHERE id = %s"

        update_fields.append(data['id'])

        execute_update_query(update_query, tuple(update_fields))
        return jsonify({'message': 'Data updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
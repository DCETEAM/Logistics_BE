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
def city_update_data():
    try:
        data = request.get_json()
        update_query = "UPDATE city SET "
        update_fields = []

        # if 'accountNumber' in data:
        #     update_query += "accountNumber = %s, "
        #     update_fields.append(data['accountNumber'])

        if 'name' in data:
            update_query += "name = %s, "
            update_fields.append(data['name'].strip())

        if 'km' in data:
            update_query += "km = %s, "
            update_fields.append(data['km'].strip())
            
            
        update_query = update_query.rstrip(', ') + " WHERE id = %s"

        update_fields.append(data['id'])

        execute_update_query(update_query, tuple(update_fields))
        return jsonify({'message': 'Data updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

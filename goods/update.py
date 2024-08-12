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
def goods_update_data():
    try:
        data = request.get_json()
        update_query = "UPDATE goods SET "
        update_fields = []

        if 'name' in data:
            update_query += "name = %s, "
            update_fields.append(data['name'].strip())

        if 'unit' in data:
            update_query += "unit = %s, "
            update_fields.append(data['unit'].strip())

        if 'bagbox' in data:
            update_query += "bagbox = %s, "
            update_fields.append(data['bagbox'].strip())
        
            
        update_query = update_query.rstrip(', ') + " WHERE id = %s"  # Update based on ID

        update_fields.append(data['id'])

        execute_update_query(update_query, tuple(update_fields))
        return jsonify({'message': 'Data updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

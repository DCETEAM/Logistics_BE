import mysql.connector
from flask import jsonify, request
from dbconfig import db_config
import json

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
def station_update_data():
    try:
        data = request.get_json()
        update_query = "UPDATE station SET "
        update_fields = []

        if 'sfrom' in data:
            update_query += "source = %s, "
            update_fields.append(data['sfrom'].strip())

        if 'sdis' in data:
            update_query += "destination	 = %s, "
            update_fields.append(data['sdis'].strip())

        if 'diskm' in data:
            update_query += "diskm= %s, "
            update_fields.append(data['diskm'].strip())

        if 'details' in data:
            details_json = json.dumps(data['details'])
            update_query += "details = %s, "
            update_fields.append(details_json)

        
        if 'id' in data:
            update_query += "id = %s, "  
            update_fields.append(data['id'])
            
        update_query = update_query.rstrip(', ') + " WHERE id = %s"

        update_fields.append(data['id'])

        execute_update_query(update_query, tuple(update_fields))
        return jsonify({'message': 'Data updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
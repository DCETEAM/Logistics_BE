import mysql.connector
from flask import jsonify, request
from dbconfig import db_config

def execute_delete_query(query, data):
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

def transporter_delete_data():
    try:
        data = request.get_json()
        delete_query = "DELETE FROM transporter WHERE id = %s"
        execute_delete_query(delete_query, (data['id'],))
        return jsonify({'message': 'Data deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
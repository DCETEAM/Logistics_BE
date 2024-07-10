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

def bill_delete_data():
    try:
        data = request.get_json()
        deleted_bill_number = data['id']
        delete_query = "DELETE FROM localbill WHERE id = %s"
        execute_delete_query(delete_query, (deleted_bill_number,))
        update_query = """
            UPDATE bill 
            SET billNumber = billNumber - 1 
            WHERE billNumber > %s
        """
        execute_update_query(update_query, (deleted_bill_number,))

        return jsonify({'message': 'Data deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

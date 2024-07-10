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
def truck_update_data():
    try:
        data = request.get_json()
        update_query = "UPDATE truck SET "
        update_fields = []

        if 'truckNumber' in data:
            update_query += "truckNumber = %s, "
            update_fields.append(data['truckNumber'])

        if 'chassisNumber' in data:
            update_query += "chassisNumber = %s, "
            update_fields.append(data['chassisNumber'])

        if 'NPEXD' in data:
            update_query += "NPEXD = %s, "
            update_fields.append(data['NPEXD'])

        if 'LPEXD' in data:
            update_query += "LPEXD = %s, "
            update_fields.append(data['LPEXD'])

        if 'fcExpiryDate' in data:
            update_query += "fcExpiryDate = %s, "
            update_fields.append(data['fcExpiryDate'])

        if 'taxExpiryDate' in data:
            update_query += "taxExpiryDate = %s, "
            update_fields.append(data['taxExpiryDate'])

        if 'insuranceExpiryDate' in data:
            update_query += "insuranceExpiryDate = %s, "
            update_fields.append(data['insuranceExpiryDate'])

        if 'registrationDate' in data:
            update_query += "registrationDate = %s, "
            update_fields.append(data['registrationDate'])    

            
        update_query = update_query.rstrip(', ') + " WHERE id = %s"
        
        update_fields.append(data['id'])

        execute_update_query(update_query, tuple(update_fields))
        return jsonify({'message': 'Data updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
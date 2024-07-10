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
def bill_update_data():
    try:
        data = request.get_json()
        update_query = "UPDATE localbill SET "
        update_fields = []

        if 'billNumber' in data:
            update_query += "billNumber = %s, "
            update_fields.append(data['billNumber'])

        if 'movementNo' in data:
            update_query += "movementNo = %s, "
            update_fields.append(data['movementNo'])

        if 'truckMovementNo' in data:
            update_query += "truckMovementNo = %s, "
            update_fields.append(data['truckMovementNo'])

        if 'party' in data:
            update_query += "party = %s, "
            update_fields.append(data['party'])

        if 'source' in data:
            update_query += "source = %s, "
            update_fields.append(data['source'])

        if 'destination' in data:
            update_query += "destination = %s, "
            update_fields.append(data['destination'])

        if 'staff' in data:
            update_query += "staff = %s, "
            update_fields.append(data['staff'])

        if 'transporter' in data:
            update_query += "transporter = %s, "
            update_fields.append(data['transporter'])

        if 'goods' in data:
            update_query += "goods = %s, "
            update_fields.append(data['goods'])

        if 'goodsType' in data:
            update_query += "goodsType = %s, "
            update_fields.append(data['goodsType'])

        if 'quantity' in data:
            update_query += "quantity = %s, "
            update_fields.append(data['quantity'])

        if 'rate' in data:
            update_query += "rate = %s, "
            update_fields.append(data['rate'])

        if 'totalAmount' in data:
            update_query += "totalAmount = %s, "
            update_fields.append(data['totalAmount'])

        if 'advance' in data:
            update_query += "advance = %s, "
            update_fields.append(data['advance'])

        if 'balance' in data:
            update_query += "balance = %s, "
            update_fields.append(data['balance'])

        if 'branch' in data:
            update_query += "branch = %s, "
            update_fields.append(data['branch'])

        if 'date1' in data:
            update_query += "date1 = %s, "
            update_fields.append(data['date1'])
            
        update_query = update_query.rstrip(', ') + " WHERE id = %s"

        update_fields.append(data['id'])

        execute_update_query(update_query, tuple(update_fields))
        return jsonify({'message': 'Data updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
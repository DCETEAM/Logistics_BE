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

def get_transporter_id(transporter_name):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        query = "SELECT id FROM transporter WHERE name = %s"
        cursor.execute(query, (transporter_name,))
        transporter_id = cursor.fetchone()[0]
        return transporter_id
    except Exception as e:
        raise e
    finally:
        cursor.close()
        connection.close()

def get_party_id(party_name):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        query = "SELECT id FROM party WHERE name = %s"
        cursor.execute(query, (party_name,))
        party_id = cursor.fetchone()[0]
        return party_id
    except Exception as e:
        raise e
    finally:
        cursor.close()
        connection.close()

def movement_update_data():
    try:
        data = request.get_json()
        update_query = "UPDATE movement SET "
        update_fields = []

        if 'transporterid' in data:
            transporterid = get_transporter_id(data['transporter'])
            update_query += "transporter = %s, "
            update_fields.append(transporterid)

        if 'partyid' in data:
            partyid = get_party_id(data['party'])
            update_query += "party = %s, "
            update_fields.append(partyid)


        if 'invoiceNumber' in data:
            update_query += "invoiceNumber = %s, "
            update_fields.append(data['invoiceNumber'])

        if 'acknowledgementNo' in data:
            update_query += "acknowledgementNo = %s, "
            update_fields.append(data['acknowledgementNo'])

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

        if 'date' in data:
            update_query += "date = %s, "
            update_fields.append(data['date'])

        if 'ownername' in data:
            update_query += "ownername = %s, "
            update_fields.append(data['ownername'])
            
        update_query = update_query.rstrip(', ') + " WHERE invoiceNumber = %s"

        update_fields.append(data['invoiceNumber'])

        execute_update_query(update_query, tuple(update_fields))
        return jsonify({'message': 'Data updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
        

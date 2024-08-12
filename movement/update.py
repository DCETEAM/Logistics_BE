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
        select_query = "SELECT * FROM localbill ORDER BY date1"
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        
        if str(data['truckMovementNo']).strip() != "0" and data['truckMovementNo'] != None and data['truckMovementNo'] != "":
            check_duplicate="SELECT * FROM movement WHERE  truckMovementNo=%s and invoiceNumber != %s"
            cursor.execute(check_duplicate,tuple([data['truckMovementNo'],data['invoiceNumber']]))   
            result = cursor.fetchall()    
                        
            if len(result):                
                return jsonify({"message":"Truck Memo number is duplicate"})
        if str(data['acknowledgementNo']).strip() != "0" and data['acknowledgementNo'] != None and data['acknowledgementNo'] != "":
            check_duplicate="SELECT * FROM movement WHERE  acknowledgementNo=%s and invoiceNumber != %s"
            cursor.execute(check_duplicate,tuple([data['acknowledgementNo'],data['invoiceNumber']]))
            result = cursor.fetchall()
                         
            if len(result):
                print("2")
                return jsonify({"message":"Acknowledgement number is duplicate"})   
        print("utr",data['utrNo'])
        if str(data['utrNo']).strip() != "0" and data['utrNo'] != None and data['utrNo'] != "":     
            check_duplicate="SELECT * FROM movement WHERE utrNo=%s and invoiceNumber != %s"     
            cursor.execute(check_duplicate,tuple([data['utrNo'],data['invoiceNumber']]))
            result = cursor.fetchall()   
            print("u",len(result))            
            if len(result):
                print("3")
                return jsonify({"message":"UTR number is duplicate"})             
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
            update_fields.append(data['invoiceNumber'].strip())

        if 'acknowledgementNo' in data:
            update_query += "acknowledgementNo = %s, "
            update_fields.append(data['acknowledgementNo'].strip())

        if 'movementNo' in data:
            update_query += "movementNo = %s, "
            update_fields.append(data['movementNo'].strip())

        if 'truckMovementNo' in data:
            update_query += "truckMovementNo = %s, "
            update_fields.append(data['truckMovementNo'].strip())

        if 'party' in data:
            update_query += "party = %s, "
            update_fields.append(data['party'].strip())

        if 'source' in data:
            update_query += "source = %s, "
            update_fields.append(data['source'].strip())

        if 'destination' in data:
            update_query += "destination = %s, "
            update_fields.append(data['destination'].strip())

        if 'staff' in data:
            update_query += "staff = %s, "
            update_fields.append(data['staff'].strip())

        if 'transporter' in data:
            update_query += "transporter = %s, "
            update_fields.append(data['transporter'].strip())

        if 'goods' in data:
            update_query += "goods = %s, "
            update_fields.append(data['goods'].strip())

        if 'goodsType' in data:
            update_query += "goodsType = %s, "
            update_fields.append(data['goodsType'].strip())

        if 'quantity' in data:
            update_query += "quantity = %s, "
            update_fields.append(data['quantity'].strip())

        if 'rate' in data:
            update_query += "rate = %s, "
            update_fields.append(data['rate'].strip())

        if 'totalAmount' in data:
            update_query += "totalAmount = %s, "
            update_fields.append(data['totalAmount'].strip())

        if 'advance' in data:
            update_query += "advance = %s, "
            update_fields.append(data['advance'].strip())

        if 'balance' in data:
            update_query += "balance = %s, "
            update_fields.append(data['balance'].strip())

        if 'branch' in data:
            update_query += "branch = %s, "
            update_fields.append(data['branch'].strip())

        if 'date' in data:
            update_query += "date = %s, "
            update_fields.append(data['date'].strip())

        if 'ownername' in data:
            update_query += "ownername = %s, "
            update_fields.append(data['ownername'].strip())
            
        if 'coolieRadio' in data:
            update_query+= "coolieType =%s,"
            update_fields.append(data['coolieRadio'].strip())
        if 'mamulRadio' in data:
            update_query+= "mamulType =%s,"
            update_fields.append(data['mamulRadio'].strip())
        if 'extraRadio' in data:
            update_query+= "extraType =%s,"
            update_fields.append(data['extraRadio'].strip())
        if 'chitcashRadio' in data:
            update_query+= "chitcashType =%s,"
            update_fields.append(data['chitcashRadio'].strip())
            
        if 'coolie' in data:
            update_query+= "coolie =%s,"
            update_fields.append(data['coolie'].strip())
        if 'mamul' in data:
            update_query+= "mamul =%s,"
            update_fields.append(data['mamul'].strip())
        if 'extra' in data:
            update_query+= "extra =%s,"
            update_fields.append(data['extra'].strip())
        if 'chitcash' in data:
            update_query+= "chitcash =%s,"
            update_fields.append(data['chitcash'].strip())
            
        if 'toll' in data:
            update_query+= "toll =%s,"
            update_fields.append(data['toll'].strip())
        if 'wayment' in data:
            update_query+= "wayment =%s,"
            update_fields.append(data['wayment'].strip())
        if 'utrNo' in data:
            update_query+= "utrNo =%s,"
            update_fields.append(data['utrNo'].strip())
        if 'utrDate' in data:
            update_query+= "utrDate =%s,"
            update_fields.append(data['utrDate'].strip())
        if 'ackDate' in data:
            update_query+= "ackDate =%s,"
            update_fields.append(data['ackDate'].strip())
        if 'totalFinalBalance' in data:
            update_query+= "totalFinalBalance =%s,"
            update_fields.append(data['totalFinalBalance'].strip())
            
        update_query = update_query.rstrip(', ') + " WHERE invoiceNumber = %s"

        update_fields.append(data['invoiceNumber'].strip())

        execute_update_query(update_query, tuple(update_fields))
        return jsonify({'message': 'Data updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
        

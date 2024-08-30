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
        if 'truckNumber' in data:
            update_query += "truckNumber = %s, "
            update_fields.append(str(data['truckNumber']).strip())
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
        if 'ActualAmount' in data:
            update_query += "ActualAmount = %s, "
            update_fields.append(data['ActualAmount'])
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
            
        if 'coolieRadio' in data:
            update_query+= "coolieType =%s,"
            update_fields.append(data['coolieRadio'])
        if 'mamulRadio' in data:
            update_query+= "mamulType =%s,"
            update_fields.append(data['mamulRadio'])
        if 'extraRadio' in data:
            update_query+= "extraType =%s,"
            update_fields.append(data['extraRadio'])
        if 'chitcashRadio' in data:
            update_query+= "chitcashType =%s,"
            update_fields.append(data['chitcashRadio'])
            
        if 'coolie' in data:
            update_query+= "coolie =%s,"
            update_fields.append(data['coolie'])
        if 'mamul' in data:
            update_query+= "mamul =%s,"
            update_fields.append(data['mamul'])
        if 'extra' in data:
            update_query+= "extra =%s,"
            update_fields.append(data['extra'])
        if 'chitcash' in data:
            update_query+= "chitcash =%s,"
            update_fields.append(data['chitcash'])
            
        if 'toll' in data:
            update_query+= "toll =%s,"
            update_fields.append(data['toll'])
        if 'wayment' in data:
            update_query+= "wayment =%s,"
            update_fields.append(data['wayment'])
        if 'utrNo' in data:
            update_query+= "utrNo =%s,"
            update_fields.append(data['utrNo'])
        if 'utrDate' in data:
            update_query+= "utrDate =%s,"
            update_fields.append(data['utrDate'])
        if 'ackDate' in data:
            update_query+= "ackDate =%s,"
            update_fields.append(data['ackDate'])
        if 'totalFinalBalance' in data:
            update_query+= "totalFinalBalance =%s,"
            update_fields.append(data['totalFinalBalance'])
            
        update_query = update_query.rstrip(', ') + " WHERE invoiceNumber = %s"

        update_fields.append(data['invoiceNumber'])

        execute_update_query(update_query, tuple(update_fields))
        return jsonify({'message': 'Data updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
        

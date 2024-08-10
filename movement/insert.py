import mysql.connector
from flask import jsonify, request
from dbconfig import db_config

def execute_insert_query(query, data):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        result = cursor.execute(query, data)
        connection.commit()
        return result
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


def insert_truck(truckNumber):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        # Check if truck number exists
        query = "SELECT * FROM truck WHERE truckNumber = %s"
        cursor.execute(query, (truckNumber,))
        existing_truck = cursor.fetchone()

        # If truck number doesn't exist, insert it
        if not existing_truck:
            insert_query = "INSERT INTO truck (truckNumber) VALUES (%s)"
            cursor.execute(insert_query, (truckNumber,))
            connection.commit()
            return True  # Return True if inserted
        else:
            return False  # Return False if not inserted
        
    except Exception as e:
        raise e
    finally:
        cursor.close()
        connection.close()

def movement_insert_data():
    try:
        data = request.get_json()
        print("Received data:", data) 
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        if str(data['truckMovementNo']).strip() != "0" and data['truckMovementNo'] != None and data['truckMovementNo'] != "":
            check_duplicate="SELECT * FROM movement WHERE  truckMovementNo=%s"
            cursor.execute(check_duplicate,tuple([data['truckMovementNo']]))   
            result = cursor.fetchall()    
                        
            if len(result):                
                return jsonify({"message":"Truck Memo number is duplicate"})
        if str(data['acknowledgementNo']).strip() != "0" and data['acknowledgementNo'] != None and data['acknowledgementNo'] != "":
            check_duplicate="SELECT * FROM movement WHERE  acknowledgementNo=%s"
            cursor.execute(check_duplicate,tuple([data['acknowledgementNo']]))
            result = cursor.fetchall()
                         
            if len(result):
                print("2")
                return jsonify({"message":"Acknowledgement number is duplicate"})   
        print("utr",data['utrNo'])
        if str(data['utrNo']).strip() != "0" and data['utrNo'] != None and data['utrNo'] != "":     
            check_duplicate="SELECT * FROM movement WHERE utrNo=%s "     
            cursor.execute(check_duplicate,tuple([data['utrNo']]))
            result = cursor.fetchall()   
            print("u",len(result))            
            if len(result):
                print("3")
                return jsonify({"message":"UTR number is duplicate"})             
        transporterid = get_transporter_id(data['transporter'])
        partyid = get_party_id(data['party'])
        invoice_parts = data['invoiceNumber'].split('/')
        invoiceNo = invoice_parts[0]
        
        truck_inserted = insert_truck(data['truckNumber'])


        insert_query = "INSERT INTO `movement` (`invoiceNumber`, `invoiceNo`,  `acknowledgementNo`, `movementNo`,`branch`, `date`, `truckNumber`, `truckMovementNo`, `party`, `partyid`, `source`,`destination`, `staff`, `transporter`, `transporterid`, `goods`, `quantity`, `rate`, `totalAmount`, `advance`, `balance`, `status`,`bags`,`ActualAmount`,`ownername`,`coolieType`,`mamulType`,`chitcashType`,`extraType`,`coolie`,`mamul`,`chitcash`,`extra`,`toll`,`wayment`,`utrNo`,`utrDate`,`ackDate`,`totalFinalBalance`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        movement_insert_data = (
            data['invoiceNumber'],
            invoiceNo,
            data['acknowledgementNo'],
            data['movementNo'],
            data['branch'], 
            data['date'], 
            data['truckNumber'],
            data['truckMovementNo'],
            data['party'],
            partyid,
            data['source'],
            data['destination'],
            data['staff'],
            data['transporter'],
            transporterid,
            data['goods'],
            data['quantity'],
            data['rate'],
            data['totalAmount'],
            data['advance'],
            data['balance'],
            data['status'],
            data['bags'],
            data['ActualAmount'],
            data['ownername'],
            data['coolieRadio'],
            data['mamulRadio'],
            data['chitcashRadio'],
            data['extraRadio'],
            data['coolie'],
            data['mamul'],
            data['chitcash'],
            data['extra'],
            data['toll'],
            data['wayment'],
            data['utrNo'],
            data['utrDate'],
            data['acknowledgementDate'],
            data['totalFinalBalance']
        )

      
        result = execute_insert_query(insert_query, movement_insert_data)
        return jsonify({'message': "Insert Success."})
       
    except Exception as e:
        print("Error inserting data:", e) 
        return jsonify({'error': str(e)})

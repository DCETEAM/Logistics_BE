import mysql.connector 
from flask import jsonify, request
from dbconfig import db_config

def execute_insert_query(query, data):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        cursor.execute(query, data)
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
        result = cursor.fetchone()
        if result:
            transporter_id = result[0]
            return transporter_id
        else:
            raise ValueError(f"Transporter '{transporter_name}' not found.")
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
        result = cursor.fetchone()
        if result:
            party_id = result[0]
            return party_id
        else:
            raise ValueError(f"Party '{party_name}' not found.")
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

        # Duplicate Checks
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        
        # Check for duplicate truckMovementNo
        if str(data.get('truckMovementNo', '').strip()) not in ["0", ""]:
            check_duplicate = "SELECT * FROM movement WHERE truckMovementNo = %s"
            cursor.execute(check_duplicate, (data['truckMovementNo'],))   
            result = cursor.fetchall()    
                        
            if len(result):                
                return jsonify({"message": "Truck Memo number is duplicate"}), 400  # Return appropriate HTTP status code

        # Check for duplicate acknowledgementNo
        if str(data.get('acknowledgementNo', '').strip()) not in ["0", ""]:
            check_duplicate = "SELECT * FROM movement WHERE acknowledgementNo = %s"
            cursor.execute(check_duplicate, (data['acknowledgementNo'],))
            result = cursor.fetchall()
                         
            if len(result):
                print("Acknowledgement number is duplicate")
                return jsonify({"message": "Acknowledgement number is duplicate"}), 400   
        
        # Check for duplicate utrNo
        if str(data.get('utrNo', '').strip()) not in ["0", ""]:
            check_duplicate = "SELECT * FROM movement WHERE utrNo = %s"     
            cursor.execute(check_duplicate, (data['utrNo'],))
            result = cursor.fetchall()   
            print("u",len(result))
            if len(result):
                print("UTR number is duplicate")
                return jsonify({"message": "UTR number is duplicate"}), 400             

        cursor.close()
        connection.close()

        # Get IDs for transporter and party
        transporterid = get_transporter_id(data['transporter'])
        partyid = get_party_id(data['party'])

        # Extract invoiceNo from invoiceNumber
        invoice_parts = data['invoiceNumber'].split('/')
        invoiceNo = invoice_parts[0]
        
        # Insert truck if not existing
        truck_inserted = insert_truck(data['truckNumber'].strip())

        # Prepare the INSERT statement
        insert_query = """
            INSERT INTO `movement` (
                `invoiceNumber`, `invoiceNo`, `acknowledgementNo`, `movementNo`,
                `branch`, `date`, `truckNumber`, `truckMovementNo`, `party`,
                `partyid`, `source`, `destination`, `staff`, `transporter`,
                `transporterid`, `goods`, `quantity`, `rate`, `totalAmount`,
                `advance`, `balance`, `status`, `bags`, `ActualAmount`,
                `ownername`, `coolieType`, `mamulType`, `chitcashType`,
                `extraType`, `coolie`, `mamul`, `chitcash`, `extra`,
                `toll`, `wayment`, `utrNo`, `utrDate`, `ackDate`, `totalFinalBalance`
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """

        movement_insert_data = (
            data.get('invoiceNumber'),
            invoiceNo,
            data.get('acknowledgementNo'),
            data.get('movementNo'),
            data.get('branch'), 
            data.get('date'), 
            data.get('truckNumber'),
            data.get('truckMovementNo'),
            data.get('party'),
            partyid,
            data.get('source'),
            data.get('destination'),
            data.get('staff'),
            data.get('transporter'),
            transporterid,
            data.get('goods'),
            data.get('quantity'),
            data.get('rate'),
            data.get('totalAmount'),
            data.get('advance'),
            data.get('balance'),
            data.get('status'),
            data.get('bags'),
            data.get('ActualAmount'),
            data.get('ownername'),
            data.get('coolieType'),
            data.get('mamulType'),
            data.get('chitcashType'),
            data.get('extraType'),
            data.get('coolie'),
            data.get('mamul'),
            data.get('chitcash'),
            data.get('extra'),
            data.get('toll'),
            data.get('wayment'),
            data.get('utrNo'),
            data.get('utrDate'),
            data.get('acknowledgementDate'),  # Mapped to `ackDate`
            data.get('totalFinalBalance')
        )

        # Execute the INSERT query
        result = execute_insert_query(insert_query, movement_insert_data)
        return jsonify({'message': "Insert Success.", 'movement_id': result}), 201  # Return appropriate HTTP status code and movement ID
       
    except Exception as e:
        print("Error inserting data:", e) 
        return jsonify({'error': str(e)}), 500  # Return appropriate HTTP status code


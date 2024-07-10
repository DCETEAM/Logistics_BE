import mysql.connector
from flask import jsonify, request
from dbconfig import db_config

def execute_select_query(query, data):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query, data)
        result = cursor.fetchall()  
        return result  
    except Exception as e:
        raise e
    finally:
        cursor.close()
        connection.close()

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

def movement_delete_data():
    try:
        data = request.get_json()
     
        invoiceNumber = data.get('invoiceNumber')
        transporterid = data.get('transporterid')
        partyid = data.get('partyid')
        
        advance = data.get('advance')
        balance = data.get('balance')

        # Check and convert advance and balance to float, set to 0 if empty
        advance = float(advance) if advance else 0.0
        balance = float(balance) if balance else 0.0

        transporter_query = "SELECT advance, balance FROM transporter WHERE id = %s"
        party_query = "SELECT balance FROM party WHERE id = %s"

        transporter_data = execute_select_query(transporter_query, (transporterid,))
        party_data = execute_select_query(party_query, (partyid,))

      
        transporter_advance, transporter_balance = (float(transporter_data[0]['advance']) if transporter_data[0]['advance'] else 0.0, 
                                                    float(transporter_data[0]['balance']) if transporter_data[0]['balance'] else 0.0) if transporter_data else (0.0, 0.0)
        party_balance = float(party_data[0]['balance']) if party_data and party_data[0]['balance'] else 0.0

      

        new_transporter_advance = max(0, transporter_advance - advance)
        new_transporter_balance = max(0, transporter_balance - balance)
        new_party_balance = max(0, party_balance - balance)
        
      

        update_transporter_query = "UPDATE transporter SET advance = %s, balance = %s WHERE id = %s"
        execute_update_query(update_transporter_query, (new_transporter_advance, new_transporter_balance, transporterid))

        update_party_query = "UPDATE party SET balance = %s WHERE id = %s"
        execute_update_query(update_party_query, (new_party_balance, partyid))

        delete_query = "DELETE FROM movement WHERE invoiceNumber = %s"
        execute_update_query(delete_query, (invoiceNumber,))

        return jsonify({'message': 'Movement deleted successfully'})
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)})


import mysql.connector
from flask import Flask, jsonify
from dbconfig import db_config

app = Flask(__name__)

def execute_query(query, params=None):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if cursor.description is not None:  
            result = cursor.fetchall()  
        else:
            result = None
        
        connection.commit()  
        return result
    except Exception as e:
        connection.rollback()  
        raise e
    finally:
        cursor.close()
        connection.close()

def update_party_table(partyid, balance):
    update_query = "UPDATE party SET balance = %s WHERE id = %s"
    params = (balance, partyid)
    execute_query(update_query, params)

def party_post_data():
    movement_data = execute_query("SELECT partyid, SUM(balance) AS total_balance FROM movement GROUP BY partyid")
    if movement_data:
        for entry in movement_data:
            partyid= entry['partyid']
            balance = entry['total_balance']
            party_entry = execute_query("SELECT id FROM party WHERE id = %s", (partyid,))
            if party_entry:
                partyid = party_entry[0]['id']
            update_party_table(partyid, balance)
        return jsonify({'message': 'party table updated successfully'})
    else:
        return jsonify({'message': 'No movement data found'})



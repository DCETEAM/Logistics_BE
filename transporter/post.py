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

def update_transporter_table(transporterid, advance, balance):
    update_query = "UPDATE transporter SET advance = %s, balance = %s WHERE id = %s"
    params = (advance, balance, transporterid)
    execute_query(update_query, params)

def transporter_post_data():
    movement_data = execute_query("SELECT transporterid, SUM(advance) AS total_advance, SUM(balance) AS total_balance FROM movement GROUP BY transporterid")
    if movement_data:
        for entry in movement_data:
            transporterid = entry['transporterid']
            advance = entry['total_advance']
            balance = entry['total_balance']
            transporter_entry = execute_query("SELECT id FROM transporter WHERE id = %s", (transporterid,))
            if transporter_entry:
                transporterid = transporter_entry[0]['id']
            update_transporter_table(transporterid, advance, balance)
        return jsonify({'message': 'Transporter table updated successfully'})
    else:
        return jsonify({'message': 'No movement data found'})



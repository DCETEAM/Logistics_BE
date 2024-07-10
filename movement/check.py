import mysql.connector
from flask import jsonify, request
from dbconfig import db_config

def execute_select_query(query, params):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query, params)
        result = cursor.fetchone()
    finally:
        cursor.close()
        connection.close()

    return result

def execute_update_query(query, params):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        cursor.execute(query, params)
        connection.commit()
    finally:
        cursor.close()
        connection.close()

def check_balance(invoiceNumber):
    select_query = "SELECT balance FROM movement WHERE invoiceNumber = %s"
    result = execute_select_query(select_query, (invoiceNumber,))
    
    if result is None:
        raise Exception("No balance found for the given invoiceNumber")

    balance = float(result['balance'])

    if balance > 0:
        return True
    else:
        return False


def move_to_completed(invoiceNumber):
    update_query = "UPDATE movement SET status = 'Completed' WHERE invoiceNumber = %s"
    execute_update_query(update_query, (invoiceNumber,))

def movement_check_data():
    if request.method == 'POST':
        invoiceNumber = request.json.get('invoiceNumber')
        try:
            statusFlag = check_balance(invoiceNumber)
            if not statusFlag:
                move_to_completed(invoiceNumber)
            
            return jsonify({'status': statusFlag})
        except Exception as e:
            return jsonify({'error': str(e)})
    else:
        return jsonify({'error': 'Only POST requests are supported for this endpoint'})

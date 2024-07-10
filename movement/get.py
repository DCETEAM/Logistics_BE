from flask import Flask, jsonify, request
import mysql.connector
from dbconfig import db_config

app = Flask(__name__)

def execute_select_query(query, params=None):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    finally:
        cursor.close()
        connection.close()

def get_movements_data(invoiceNumber):
    select_query = """
    SELECT 
        movement.advance AS advance,
        movement.balance AS balance
    FROM 
        movement 
    WHERE 
        movement.invoiceNumber = %s
    """
    try:
        print("Executing query:", select_query)
        result = execute_select_query(select_query, (invoiceNumber,))
        print("Query result:", result)
        return result[0]  
    except Exception as e:
        print("Error:", e)
        return {'error': str(e)}

@app.route('/movement')
def get_movements_handler():
    invoiceNumber = request.args.get('invoiceNumber')
    if not invoiceNumber:
        return jsonify({'error': 'Invoice number is required.'}), 400
    
    return jsonify(get_movements_data(invoiceNumber)), 200

if __name__ == '__main__':
    app.run(debug=True)

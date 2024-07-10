import mysql.connector
from flask import jsonify, request
from dbconfig import db_config
from datetime import datetime


def execute_select_query(query):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    finally:
        cursor.close()
        connection.close()  

def get_fiscal_year():
    today = datetime.now()
    month = today.month

    fiscal_year_start = fiscal_year_end = today.year
    if month < 4:
        fiscal_year_start -= 1
    else:
        fiscal_year_end += 1
    return fiscal_year_start, fiscal_year_end        

def movement_fetches_data():
    try:
        select_query = "SELECT invoiceNo FROM movement ORDER BY invoiceNo DESC LIMIT 1"
        result = execute_select_query(select_query)
        
        if result:
            last_invoice_number = result[0]['invoiceNo']
            next_numeric_part = last_invoice_number + 1
        else:
            next_numeric_part = 1

        goods_value = request.form.get('goods') 
        fiscal_year_start, fiscal_year_end = get_fiscal_year()
        fiscal_year_str = f"{fiscal_year_start}-{fiscal_year_end}"
        
        new_invoice_number = f"{next_numeric_part}/{goods_value}/{fiscal_year_str}"
        
        return jsonify({'new_invoice_number': new_invoice_number})
    
    except Exception as e:
        return jsonify({'error': str(e)})


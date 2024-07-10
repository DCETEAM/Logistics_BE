from flask import request, jsonify
from datetime import datetime
import mysql.connector
from dbconfig import db_config


def execute_query(query, data):
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

def calculate_billnumber_data():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        date_str = request.json.get('date')
        if not date_str:
            return None, "Date is required"

        date = datetime.strptime(date_str, '%Y-%m-%d')

        formatted_date = date.strftime('%Y-%m-%d')

        
        current_date_query = "SELECT COUNT(*) FROM localbill WHERE date1 = %s"
        cursor.execute(current_date_query, (formatted_date,))
        count = cursor.fetchone()[0]

        if count > 0:
            current_date_max_query = "SELECT MAX(billNumber) FROM localbill WHERE date1 = %s"
            cursor.execute(current_date_max_query, (formatted_date,))
            current_date_max_bill_number = cursor.fetchone()[0]
            bill_no = str(int(current_date_max_bill_number) + 1)
        else:
            
            prev_date_query = "SELECT MAX(date1) FROM localbill WHERE date1 < %s"
            cursor.execute(prev_date_query, (formatted_date,))
            prev_date_result = cursor.fetchone()[0]

            if prev_date_result:
                
                prev_date = datetime.strptime(prev_date_result, '%Y-%m-%d')
                prev_formatted_date = prev_date.strftime('%Y-%m-%d')
                prev_query = "SELECT MAX(billNumber) FROM localbill WHERE date1 = %s"
                cursor.execute(prev_query, (prev_formatted_date,))
                prev_max_bill_number = cursor.fetchone()[0]

                if prev_max_bill_number is not None:
                    bill_no = str(int(prev_max_bill_number) + 1)
                else:
                    bill_no = "1"
            else:
                bill_no = "1"

        
            connection.commit()
        return bill_no, None
    except mysql.connector.Error as error:
        print("Error calculating bill number:", error)
        return None, "Error calculating bill number"
    finally:
        cursor.close()
        connection.close()



def calculate_billnumber_handler():
    if request.method == 'OPTIONS':
        return jsonify({"message": "OK"}), 200

    try:
        bill_no, error_message = calculate_billnumber_data()
        if error_message:
            return jsonify({"message": error_message}), 500

        return jsonify({"billNumber": bill_no}), 200
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({"message": "An error occurred while processing the request"}), 500
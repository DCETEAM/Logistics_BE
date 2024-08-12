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

def bill_insert_data():
    try:
        data = request.get_json()
        print("Received data:", data) 

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        formatted_date = data['billNumber'].strip()
        future_bills_query = "SELECT date1, billNumber FROM localbill WHERE billNumber >= %s ORDER BY billNumber DESC"
        cursor.execute(future_bills_query, (formatted_date,))
        future_bills = cursor.fetchall()
        
        print("Fetched future bills:", future_bills)

        for future_bill in future_bills:
            future_bill_date = future_bill[0]
            future_bill_number = future_bill[1]   
            new_bill_number = str(int(future_bill_number) + 1)    

            print("New BillNumber", new_bill_number, " Prev BillNumner:", future_bill_number)
            update_query = "UPDATE localbill SET billNumber = %s WHERE billNumber = %s"
            cursor.execute(update_query, (new_bill_number, future_bill_number))

            # print("Updated bill with new bill number:", new_bill_number)

        connection.commit()
        cursor.close()
        connection.close()

        insert_query = "INSERT INTO `localbill` (`billNumber`, `movementNo`, `branch`, `date1`, `truckNumber`, `truckMovementNo`, `party`, `source`, `destination`, `staff`, `transporter`, `goods`, `goodsType`, `quantity`, `rate`, `totalAmount`, `advance`, `balance`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        bill_insert_data = (
            data['billNumber'].strip(),
            data['movementNo'].strip(),
            data['branch'].strip(), 
            data['date1'].strip(), 
            data['truckNumber'].strip(),
            data['truckMovementNo'].strip(),
            data['party'].strip(),
            data['source'].strip(),
            data['destination'].strip(),
            data['staff'].strip(),
            data['transporter'].strip(),
            data['goods'].strip(),
            data['goodsType'].strip(),
            data['quantity'].strip(),
            data['rate'].strip(),
            data['totalAmount'].strip(),
            data['advance'].strip(),
            data['balance'].strip(),
        )
        result = execute_insert_query(insert_query, bill_insert_data)

        return jsonify({'message': "Insert Success."})
    except Exception as e:
        print("Error inserting data:", e) 
        return jsonify({'error': str(e)})

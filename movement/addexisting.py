import mysql.connector
import json
from flask import jsonify, request
from dbconfig import db_config

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

def execute_insert_query(query, data):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        cursor.execute(query, data)
        connection.commit()
    finally:
        cursor.close()
        connection.close()

def execute_update_query(query):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        cursor.execute(query)
        connection.commit()
    finally:
        cursor.close()
        connection.close()

def update_bill_number(new_bill_number, invoice_number):
    update_query = f"UPDATE movement SET billNumber = {new_bill_number} WHERE invoiceNo = {invoice_number}"
    print("Updating bill number with query:", update_query)

    execute_update_query(update_query)

def get_movement_by_invoice_number(invoice_number):
    select_query = f"SELECT * FROM movement WHERE invoiceNo = {invoice_number}"
    return execute_select_query(select_query)

def get_all_station_data():
    select_query = "SELECT * FROM station"
    return execute_select_query(select_query)

def parse_details(details):
    try:
        return json.loads(details)
    except json.JSONDecodeError:
        return []

def insert_bill_record(bill_number, movement):
    insert_query = """
     INSERT INTO `bill`( `date`, `truck`, `ackno`, `truckmo`, `party`, `source`, `destination`, `distanceKm`, `rate`, `quantity`, `billnum`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    data = (
        movement['date'],
        movement['truckNumber'],
        movement['acknowledgementNo'],
        movement['truckMovementNo'],
        movement['party'],
        movement['source'],
        movement['destination'],
        movement['diskm'],
        movement['rate'],
        movement['quantity'],
        bill_number,
    )
    execute_insert_query(insert_query, data)

def match_station_and_movement(movement, station_data):
    source = movement['source']
    destination = movement['destination']
    party = movement['party']
   
    for station in station_data:
        if station['source'] == source or station['destination'] == destination:
            details = parse_details(station['details'])
            diskm = station['diskm']
            for detail in details:
                if detail['party'] == party:
                    return detail['rate'], diskm
    return 0, 0

def movement_addexisting_data():
    try:
        selected_movements = request.json.get('selectedMovements')
        if not selected_movements:
            return jsonify({'error': 'No movements selected'}), 400

        new_bill_number = request.json.get('billNumber')
        movements_data = []
        station_data = get_all_station_data()

        for movement in selected_movements:
            invoice_parts = movement.split('/')
            invoice_no = invoice_parts[0]

            # Update bill number
            update_bill_number(new_bill_number, invoice_no)

            # Get movement details
            movement_data = get_movement_by_invoice_number(invoice_no)
            for move in movement_data:
                rate, diskm = match_station_and_movement(move, station_data)
                move['rate'] = rate
                move['diskm'] = diskm

            # Add movement data to the list
            movements_data.extend(movement_data)
            
            # Insert each movement record individually
            for move in movement_data:
                insert_bill_record(new_bill_number, move)

        return jsonify({'billNumber': new_bill_number, 'movements': movements_data})
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

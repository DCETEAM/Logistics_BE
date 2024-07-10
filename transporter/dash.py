import mysql.connector
from dbconfig import db_config  

def execute_select_query(query):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else 0
    finally:
        cursor.close()
        connection.close()

def transporter_getcount_data():
    query = "SELECT COUNT(*) FROM transporter"
    truck_count = execute_select_query(query)
    return truck_count

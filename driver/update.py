import mysql.connector
from flask import jsonify, request
from dbconfig import db_config

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
def driver_update_data():
    try:
        data = request.get_json()
        update_query = "UPDATE driver SET "
        update_fields = []

        if 'mobileNumber' in data:
            update_query += "mobileNumber = %s, "
            update_fields.append(data['mobileNumber'].strip())

        if 'licenseNumber' in data:
            update_query += "licenseNumber = %s, "
            update_fields.append(data['licenseNumber'].strip())

        if 'phoneNo' in data:
            update_query += "phoneNo = %s, "
            update_fields.append(data['phoneNo'].strip())

        if 'name' in data:
            update_query += "name = %s, "
            update_fields.append(data['name'].strip())

        if 'accountNumber' in data:
            update_query += "accountNumber = %s, "
            update_fields.append(data['accountNumber'].strip())

        if 'dateOfBirth' in data:
            update_query += "dateOfBirth = %s, "
            update_fields.append(data['dateOfBirth'].strip())

        if 'mobileNo' in data:
            update_query += "mobileNo = %s, "
            update_fields.append(data['mobileNo'].strip())
      
        if 'licenseIssueDate' in data:
            update_query += "licenseIssueDate = %s, "
            update_fields.append(data['licenseIssueDate'].strip())

        if 'licenseExpiryDate' in data:
            update_query += "licenseExpiryDate = %s, "
            update_fields.append(data['licenseExpiryDate'].strip())

        if 'dateOfJoining' in data:
            update_query += "dateOfJoining = %s, "
            update_fields.append(data['dateOfJoining'].strip())

        if 'branch' in data:
            update_query += "branch = %s, "
            update_fields.append(data['branch'].strip())

        if 'referredBy' in data:
            update_query += "referredBy = %s, "
            update_fields.append(data['referredBy'].strip())

        if 'accountHolderName' in data:
            update_query += "accountHolderName = %s, "
            update_fields.append(data['accountHolderName'].strip())

        if 'ifscCode' in data:
            update_query += "ifscCode = %s, "
            update_fields.append(data['ifscCode'].strip())

        if 'address' in data:
            update_query += "address = %s, "
            update_fields.append(data['address'].strip())            



            
        update_query = update_query.rstrip(', ') + " WHERE id = %s"

        update_fields.append(data['id'])

        execute_update_query(update_query, tuple(update_fields))
        return jsonify({'message': 'Data updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
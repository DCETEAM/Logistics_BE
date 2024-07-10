from flask import Flask
from flask import Flask, request, jsonify
from truck.insert import truck_insert_data
from truck.fetch import truck_get_data
from truck.dash import truck_getcount_data
from truck.update import truck_update_data
from truck.delete import truck_delete_data
from truck.search import truck_search_data
from staff.insert import staff_insert_data
from staff.fetch import staff_get_data
from staff.update import staff_update_data
from staff.delete import staff_delete_data
from staff.dash import staff_getcount_data
from driver.insert import driver_insert_data
from driver.fetch import driver_get_data
from driver.update import driver_update_data
from driver.delete import driver_delete_data
from party.insert import party_insert_data
from party.fetch import party_get_data
from party.update import party_update_data
from party.delete import party_delete_data
from party.dash import party_getcount_data
from accounts.insert import accounts_insert_data
from accounts.fetch import accounts_get_data
from accounts.update import accounts_update_data
from accounts.delete import accounts_delete_data
from transporter.insert import transporter_insert_data
from transporter.fetch import transporter_get_data
from transporter.update import transporter_update_data
from transporter.delete import transporter_delete_data
from transporter.dash import transporter_getcount_data
from transporter.post import transporter_post_data
from city.insert import city_insert_data
from city.fetch import city_get_data
from city.update import city_update_data
from city.delete import city_delete_data
from goods.insert import goods_insert_data
from goods.fetch import goods_get_data
from goods.update import goods_update_data
from goods.delete import goods_delete_data
from movement.insert import movement_insert_data
from movement.fetch import movement_get_data
from movement.invn import movement_fetches_data
from movement.check import movement_check_data
from movement.update import movement_update_data
from movement.delete import movement_delete_data
from movement.generate import movement_generate_data
from movement.addexisting import movement_addexisting_data
from movement.post import movement_post_data
from movement.get import get_movements_data
from bill.insert import bill_insert_data
from bill.fetch import bill_get_data
from bill.update import bill_update_data
from bill.delete import bill_delete_data
from bill.calculate import calculate_billnumber_data
from party.post import party_post_data
from station.add import station_insert_data
from station.fetch import station_get_data
from station.delete import station_delete_data
from station.update import station_update_data
from login.login import login_data
from swastik.insert import owner_insert_data
from swastik.update import owner_update_data
from swastik.fetch import owner_get_data
from swastik.delete import owner_delete_data
from billmovement.fetch import billmovement_get_data
from billmovement.update import billmovement_update_data
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/truck/insert', methods=['POST'])
def truck_insert_handler():
    return truck_insert_data()

@app.route('/truck/fetch', methods=['GET'])
def truck_fetch_handler():
    return truck_get_data()

@app.route('/truck/update', methods=['PUT'])
def truck_update_handler():
    return truck_update_data()

@app.route('/truck/delete', methods=['POST'])
def truck_delete_handler():
    return truck_delete_data()

@app.route('/truck/dash', methods=['GET'])
def truck_count():
    count = truck_getcount_data()
    return jsonify({'count': count})

@app.route('/staff/insert', methods=['POST'])
def staff_insert_handler():
    return staff_insert_data()

@app.route('/staff/fetch', methods=['GET'])
def staff_fetch_handler():
    return staff_get_data()

@app.route('/staff/update', methods=['PUT'])
def staff_update_handler():
    return staff_update_data()

@app.route('/staff/delete', methods=['POST'])
def staff_delete_handler():
    return staff_delete_data()

@app.route('/staff/dash', methods=['GET'])
def staff_count():
    count = staff_getcount_data()
    return jsonify({'count': count})

@app.route('/driver/insert', methods=['POST'])
def driver_insert_handler():
    return driver_insert_data()

@app.route('/driver/fetch', methods=['GET'])
def driver_fetch_handler():
    return driver_get_data()

@app.route('/driver/update', methods=['PUT'])
def driver_update_handler():
    return driver_update_data()

@app.route('/driver/delete', methods=['POST'])
def driver_delete_handler():
    return driver_delete_data()

@app.route('/party/insert', methods=['POST'])
def party_insert_handler():
    return party_insert_data()

@app.route('/party/fetch', methods=['GET'])
def party_fetch_handler():
    return party_get_data()

@app.route('/party/update', methods=['PUT'])
def party_update_handler():
    return party_update_data()

@app.route('/party/delete', methods=['POST'])
def party_delete_handler():
    return party_delete_data()

@app.route('/party/dash', methods=['GET'])
def party_count():
    count = party_getcount_data()
    return jsonify({'count': count})


@app.route('/accounts/insert', methods=['POST'])
def accounts_insert_handler():
    return accounts_insert_data()

@app.route('/accounts/fetch', methods=['GET'])
def accounts_fetch_handler():
    return accounts_get_data()

@app.route('/accounts/update', methods=['PUT'])
def accounts_update_handler():                    
    return accounts_update_data()            

@app.route('/accounts/delete', methods=['POST'])
def accounts_delete_handler():
    return accounts_delete_data()

@app.route('/transporter/insert', methods=['POST'])
def  transporter_insert_handler():
    return  transporter_insert_data()

@app.route('/transporter/fetch', methods=['GET'])
def  transporter_fetch_handler():
    return  transporter_get_data()

@app.route('/transporter/update', methods=['PUT'])
def  transporter_update_handler():                 
    return  transporter_update_data()            

@app.route('/transporter/delete', methods=['POST'])
def  transporter_delete_handler():
    return transporter_delete_data()

@app.route('/transporter/dash', methods=['GET'])
def transporter_count():
    count = transporter_getcount_data()
    return jsonify({'count': count})

@app.route('/city/insert', methods=['POST'])
def city_insert_handler():
    return city_insert_data()

@app.route('/city/fetch', methods=['GET'])
def city_fetch_handler():
    return city_get_data()

@app.route('/city/update', methods=['PUT'])
def city_update_handler():                   
    return city_update_data()            

@app.route('/city/delete', methods=['POST'])
def city_delete_handler():
    return city_delete_data()

@app.route('/goods/insert', methods=['POST'])
def goods_insert_handler():
    return goods_insert_data()

@app.route('/goods/fetch', methods=['GET'])
def goods_fetch_handler():
    return goods_get_data()

@app.route('/goods/update', methods=['PUT'])
def goods_update_handler():                    
    return goods_update_data()            

@app.route('/goods/delete', methods=['POST'])
def goods_delete_handler():
    return goods_delete_data()

@app.route('/movement/insert', methods=['POST'])
def movement_insert_handler():
    return movement_insert_data()

@app.route('/movement/fetch', methods=['GET'])
def movement_fetch_handler():
    return movement_get_data()

@app.route('/movement/invn', methods=['GET'])
def movement_fetches_handler():
    return movement_fetches_data()

@app.route('/movement/check', methods=['POST'])
def movement_check_handler():
    return movement_check_data()

@app.route('/movement/update', methods=['PUT'])
def movement_update_handler():
    return movement_update_data()

@app.route('/movement/delete', methods=['POST'])
def movement_delete_handler():
    return movement_delete_data()

@app.route('/movement/generate', methods=['POST'])
def movement_generate_handler():
    return movement_generate_data()

@app.route('/movement/addexisting', methods=['POST'])
def movement_addexisting_handler():
    return movement_addexisting_data()

@app.route('/movement/post', methods=['POST'])
def movement_bill_handler():
    return movement_post_data()

@app.route('/movement/get', methods=['GET'])
def get_movements_handler():
     invoiceNumber = request.args.get('invoiceNumber')
     return jsonify(get_movements_data(invoiceNumber))

@app.route('/bill/insert', methods=['POST'])
def bill_insert_handler():
    return bill_insert_data()

@app.route('/bill/fetch', methods=['GET'])
def bill_fetch_handler():
    return bill_get_data()


@app.route('/bill/update', methods=['PUT'])
def bill_update_handler():
    return bill_update_data()

@app.route('/bill/delete', methods=['POST'])
def bill_delete_handler():
    return bill_delete_data()

@app.route('/bill/calculate', methods=['POST'])
def calculate_billnumber_handler():
    return calculate_billnumber_data()

@app.route('/transporter/post', methods=['POST'])
def transporter_post_handler():
    return transporter_post_data()

@app.route('/party/post', methods=['POST'])
def party_gets_handler():
    return party_post_data()

@app.route('/station/add', methods=['POST'])
def station_insert_handler():
    return station_insert_data()

@app.route('/station/fetch', methods=['GET'])
def station_fetch_handler():
    return station_get_data()

@app.route('/station/delete', methods=['POST'])
def station_delete_handler():
    return station_delete_data()


@app.route('/station/update', methods=['PUT'])
def station_update_handler():
    return station_update_data()


@app.route('/login/login',  methods=['POST'])
def Login_handler():
    return login_data()


@app.route('/owner/insert', methods=['POST'])
def owner_insert_handler():
    return owner_insert_data()

@app.route('/owner/fetch', methods=['GET'])
def owner_fetch_handler():
    return owner_get_data()

@app.route('/owner/update', methods=['PUT'])
def owner_update_handler():                   
    return owner_update_data()            

@app.route('/owner/delete', methods=['POST'])
def owner_delete_handler():
    return owner_delete_data()

@app.route('/billmovement/fetch', methods=['GET'])
def billmovement_fetch_handler():
    return billmovement_get_data()

@app.route('/billmovement/update', methods=['PUT'])
def billmovement_update_handler():                   
    return  billmovement_update_data()            


if __name__ == '__main__':
    app.run(debug=True)

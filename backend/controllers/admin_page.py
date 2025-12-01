from flask import Blueprint, render_template, redirect, url_for,session,request,flash
from functools import wraps
from flask import jsonify
from .__init__ import conn_database
import sqlite3
from datetime import datetime




admin_view = Blueprint('admin',__name__)


#decorator to check if admin is logged in before accessing the below routes


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id' not in session or session.get('is_admin') != True:
            return jsonify({"message": "Admin Access Required", "redirect_to": "/login"}), 403
        return f(*args, **kwargs)
    return decorated_function


@admin_view.route('/api/admin/home', methods=['GET'])
@admin_required
def admin_home():
    conn=conn_database()  
    curr=conn.cursor()
    curr.execute('SELECT * FROM PARKING_LOT')
    lots = [dict(row) for row in curr.fetchall()]
    spots=[]
    for lot in lots:
        curr.execute('SELECT PS.id,PS.lot_id,PS.spot_number,PS.status,BD.id as bid,U.email as email,BD.spot_number as sn,BD.timestamp_booked as tb,BD.vehicle_number as VN FROM PARKING_SPOT PS LEFT JOIN (SELECT * FROM BOOKING_DETAILS WHERE booking_status ="open" GROUP BY lot_id,spot_number) AS BD ON BD.spot_number = PS.spot_number AND BD.lot_id = PS.lot_id LEFT JOIN USERS U ON U.id=BD.user_id WHERE PS.lot_id =?',(lot['id'],))
        lot_spots = [dict(row) for row in curr.fetchall()]
        spots.extend(lot_spots)
    conn.close()
    return jsonify({"lots": lots, "spots": spots}), 200

@admin_view.route('/api/admin/lot/create', methods=['POST'])
@admin_required
def create_lot():
    prime_location = request.form['prime_location']
    address = request.form['address']
    pincode = request.form['pincode']
    price = request.form['price']
    max_no_of_spots = request.form['max_no_of_spots']
    if int(max_no_of_spots) < 1:
        return jsonify({"message": "Spots must be > 0"}), 400
    conn = conn_database()
    curr = conn.cursor()
    try:
        curr.execute('INSERT INTO PARKING_LOT (prime_location,price ,address,pincode,max_no_of_spots,no_of_available) VALUES (?,?,?,?,?,?)',(prime_location,price,address,pincode,max_no_of_spots,max_no_of_spots))
        id = curr.lastrowid
        for i in range(1,int(max_no_of_spots)+1):
            spot_name = f"{prime_location}_{id}_Spot # {i}"
            curr.execute('INSERT INTO PARKING_SPOT (lot_id,spot_number,status) VALUES (?,?,?)',(id,spot_name,"A"))
        conn.commit()
        conn.close()
        return jsonify({"message": "Lot Created Successfully"}), 200
    except sqlite3.IntegrityError:
        return jsonify({"message": "A Lot with this location already exists"}), 409
    except Exception as e:        
        return jsonify({"message": str(e)}), 500
    finally:
        if conn:
            conn.close()
    
@admin_view.route('/api/admin/lot/update', methods=['POST'])
@admin_required
def update_lot():
    data = request.get_json()

    lot_id = data.get('id')
    prime_location = data.get('prime_location')
    address = data.get('address')
    pincode = data.get('pincode')
    price = int(data.get('price'))
    max_no_of_spots = int(data.get('max_no_of_spots'))

    conn = conn_database()
    curr = conn.cursor()

    curr.execute('SELECT COUNT(*) FROM PARKING_SPOT WHERE lot_id = ?',(lot_id,))
    previous_total_spots = int(curr.fetchone()[0])
    curr.execute('SELECT COUNT(*) FROM PARKING_SPOT WHERE lot_id = ? and status ="O"',(lot_id,))
    no_occupied = int(curr.fetchone()[0])

    if max_no_of_spots< 0:
        conn.close()
        return jsonify({"message": "Number of spots cannot be negative"}), 400
    
    if no_occupied == 0 and max_no_of_spots ==0:
        curr.execute('DELETE FROM PARKING_SPOT WHERE lot_id =?',(lot_id,))
        curr.execute('DELETE FROM PARKING_LOT WHERE id =?',(lot_id,))
        conn.close()
        return jsonify({"message": "Lot Updated"}), 200
    if max_no_of_spots< no_occupied:
        conn.close()
        return jsonify({"message": f"Cannot reduce spots below {no_occupied} (Currently Occupied)"}), 400

    curr.execute('UPDATE PARKING_LOT SET prime_location=?,price=?,address=?,pincode=?,max_no_of_spots=?, no_of_available = ? WHERE id =?',(prime_location,price,address,pincode,max_no_of_spots,max_no_of_spots-no_occupied,lot_id))
    if max_no_of_spots < previous_total_spots:
        spots_to_remove = previous_total_spots - max_no_of_spots
        curr.execute('''
            SELECT id FROM PARKING_SPOT 
            WHERE lot_id = ? AND status = 'A' 
            ORDER BY CAST(SUBSTR(spot_number, INSTR(spot_number, '-') + 1) AS INTEGER) DESC 
            LIMIT ?
        ''', (lot_id, spots_to_remove))
        removable_spot_ids = curr.fetchall()

        for spot_id in removable_spot_ids:
            curr.execute('DELETE FROM PARKING_SPOT WHERE id = ?', (spot_id[0],))
        conn.commit()
        conn.close()
        return jsonify({"message": "Lot Updated"}), 200
    elif max_no_of_spots>=previous_total_spots:
        curr.execute('SELECT spot_number FROM PARKING_SPOT WHERE lot_id = ?', (lot_id,))
        existing_spots = curr.fetchall()
        last_spot_num = max([int(spot[0].split('#')[-1].strip()) for spot in existing_spots if '#' in spot[0]],
        default=0
        )
        for i in range(last_spot_num+1,last_spot_num+(max_no_of_spots-previous_total_spots)+1):
            j = previous_total_spots
            spot_name = f"{prime_location}_{lot_id}_Spot # {i}"
            curr.execute('INSERT INTO PARKING_SPOT (lot_id,spot_number,status) VALUES (?,?,?)',(lot_id,spot_name,'A'))
        conn.commit()
        conn.close()
        return jsonify({"message": "Lot Updated"}), 200
    
@admin_view.route('/api/admin/lot/delete', methods=['POST'])
@admin_required
def delete_lot():    
    lot_id = request.get_json().get('lot_id')
    conn = conn_database()
    curr = conn.cursor()
    curr.execute('SELECT COUNT(*) FROM PARKING_SPOT WHERE lot_id = ? and status ="O"',(lot_id,))
    no_occupied = int(curr.fetchone()[0])
    if no_occupied == 0:
        curr.execute('DELETE FROM PARKING_SPOT WHERE lot_id =?',(lot_id,))
        curr.execute('DELETE FROM PARKING_LOT WHERE id=?',(lot_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Lot Deleted"}), 200
    else:
        conn.close()
        return jsonify({"message": "Cannot delete lot with occupied spots"}), 400

@admin_view.route('/api/admin/spot/delete', methods=['POST'])
@admin_required
def delete_spot():
    data = request.get_json()
    conn = conn_database()
    curr = conn.cursor()
    curr.execute('DELETE FROM PARKING_SPOT WHERE spot_number = ? AND lot_id = ?', (data['spot_id'],))
    curr.execute('UPDATE PARKING_LOT SET max_no_of_spots= max_no_of_spots - 1, no_of_available=no_of_available-1 WHERE id = ?',(data['lot_id'],))

    conn.commit()
    conn.close()
    return jsonify({"message": "Spot Deleted"}), 200

@admin_view.route('/api/admin/users', methods=['GET'])
@admin_required
def user_management():
    conn = conn_database()
    curr = conn.cursor()
    curr.execute('SELECT * FROM USERS WHERE id!=0')
    user_list = [dict(row) for row in curr.fetchall()]
    conn.close()

    return jsonify(user_list), 200


@admin_view.route('/api/admin/search',methods=['POST'])
@admin_required
def admin_search_data():
    results = None
    data = request.get_json()
    field = data.get('field')
    value = data.get('value')
    conn=conn_database()
    curr=conn.cursor()
    if field == 'email':
        curr.execute(f"SELECT U.id as 'User ID',U.email as 'Email Address',U.name as 'Name',U.address as 'Address',U.pincode as 'Pincode',COUNT(CASE WHEN B.booking_status ='open' THEN 1 END) AS 'No of Active Bookings', COUNT(CASE WHEN B.booking_status ='closed' THEN 1 END) AS 'No of Past Bookings' FROM USERS U LEFT JOIN BOOKING_DETAILS B ON U.id = B.user_id WHERE {field} LIKE ? GROUP BY U.id,U.email,U.name,U.address",('%'+value+'%',))
    if field == 'prime_location':
        curr.execute(f"SELECT P.id as 'Parking Lot ID',P.prime_Location as 'Lot Prime Location Name',P.address as 'Lot Address',P.pincode as 'Lot Pincode',P.max_no_of_spots as 'Total Spots in Lot',P.no_of_available as 'Available Spots in Lot', P.price as 'Price per hour' FROM PARKING_LOT P WHERE {field} LIKE ? ",('%'+value+'%',))
    if field == 'spot_number':
        curr.execute(f"SELECT P.id as 'Parking Spot ID',P.spot_number as 'Spot Number',PL.prime_location as 'Lot Prime Location',PL.address as 'Lot Address',PL.pincode as 'Lot Pincode',CASE WHEN P.status='O' THEN 'Occupied' WHEN P.status = 'A' THEN 'Available' ELSE 'Unkown' END as 'Spot Status' FROM PARKING_SPOT P JOIN PARKING_LOT PL ON PL.id = P.lot_id WHERE {field} LIKE ? ",('%'+value+'%',))
    if field == 'vehicle_number':
        curr.execute(f"SELECT B.id as 'Booking ID',B.vehicle_number as 'Vehicle Number',U.email as 'User Email',U.name as 'User Name',B.spot_number as 'Spot Number',PL.prime_location as 'Lot Prime Location Name',CASE WHEN B.timestamp_booked IS NOT NULL THEN datetime(B.timestamp_booked,'unixepoch') ELSE '-' END AS 'Parking Time', CASE WHEN B.timestamp_released IS NOT NULL AND B.timestamp_released !='' THEN B.timestamp_released ELSE '-' END AS 'Release Time',CASE WHEN B.booking_status='open' THEN 'Occupied' WHEN B.booking_status = 'closed' THEN 'Parked Out' ELSE 'Unkown' END as 'Spot Status' FROM BOOKING_DETAILS B JOIN PARKING_SPOT P ON P.spot_number = B.spot_number AND P.lot_id = B.lot_id JOIN PARKING_LOT PL ON PL.id=P.lot_id  JOIN USERS U on U.id=B.user_id WHERE {field} LIKE ? ",('%'+value+'%',))
    
    rows = curr.fetchall()
    results = [dict(row) for row in rows]
    
    conn.close()
    return jsonify({"results": results}), 200
    #return render_template('admin/admin_search.html',results=results,columns=columns)

@admin_view.route('/api/admin/summary', methods=['GET'])
@admin_required
def admin_summary_data():
    conn = conn_database()
    curr = conn.cursor()

    stats = {}

    curr.execute("SELECT COUNT(*) FROM USERS WHERE is_admin=0")
    stats['total_users'] = curr.fetchone()[0]

    curr.execute("SELECT COUNT(*) FROM USERS WHERE is_admin=1")
    stats['total_admins'] =curr.fetchone()[0]

    curr.execute("SELECT COUNT(*) FROM PARKING_LOT")
    stats['total_lots']= curr.fetchone()[0]

    curr.execute("SELECT COUNT(*) FROM PARKING_SPOT")
    stats['total_spots'] = curr.fetchone()[0]

    curr.execute("SELECT COUNT(*) FROM PARKING_SPOT WHERE status='A'")
    stats['available_spots'] = curr.fetchone()[0]

    curr.execute("SELECT COUNT(*) FROM BOOKING_DETAILS")
    stats['booked_spots'] = curr.fetchone()[0]

    curr.execute("SELECT COUNT(*) FROM BOOKING_DETAILS WHERE booking_status='open'")
    stats['active_bookings'] = curr.fetchone()[0]

    curr.execute('''
        SELECT id, prime_location, max_no_of_spots, no_of_available, price FROM PARKING_LOT
    ''')
    lot_data = [dict(row) for row in curr.fetchall()]


    curr.execute('''
        SELECT U.name, B.vehicle_number, B.spot_number, B.timestamp_booked, B.booking_status, P.lot_id
        FROM BOOKING_DETAILS B
        JOIN USERS U ON B.user_id = U.id
        JOIN PARKING_SPOT P ON B.spot_number = P.spot_number AND P.lot_id = B.lot_id
        ORDER BY B.timestamp_booked DESC LIMIT 10
    ''')
    recent_bookings = [dict(row) for row in curr.fetchall()]

    conn.close()
    return jsonify({"stats": stats, "lot_data": lot_data, "recent_bookings": recent_bookings}), 200

@admin_view.route('/api/admin/profile',methods=['POST','GET'])
@admin_required
def admin_profile():
    conn = conn_database()
    curr = conn.cursor()
    curr.execute('SELECT * FROM USERS WHERE id = ?',(session['id'],))
    admin = dict(row) if row else {}
    conn.close()

    id = admin['id']
    
    if request.method == 'POST':
        data = request.get_json()
        

        conn = conn_database()
        curr = conn.cursor()

        curr.execute("UPDATE USERS SET email = ?, name = ?, address = ?, pincode = ? WHERE id = ?",
                     (data['email'], data['name'], data['address'], data['pincode'], session['id']))
        conn.commit()
        conn.close()
        return jsonify({"message": "Profile Updated Successfully"}), 200
    
    return jsonify(admin), 200

@admin_view.route('/api/admin/logout', methods=['GET'])
@admin_required
def admin_logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200
    


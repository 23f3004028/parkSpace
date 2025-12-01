from flask import Blueprint,session,request,jsonify
from .__init__ import conn_database
from functools import wraps
from datetime import datetime

user_view = Blueprint('user',__name__)

#decorator function for login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id' not in session:
            return jsonify({"message": "Authentication Required", "redirect_to": "/login"}), 401
        return f(*args, **kwargs)
    return decorated_function



@user_view.route('/api/user/home', methods=['GET'])
@login_required
def user_home():
    conn = conn_database()
    curr = conn.cursor()
    curr.execute('SELECT * FROM PARKING_LOT')
    parking_lots = curr.fetchall()#raw lots
    available_slot_data = []#lots
    for lot in parking_lots:
        lot_dict = dict(lot) 
        curr.execute("SELECT * FROM PARKING_SPOT WHERE lot_id = ? AND status = 'A' LIMIT 1",(lot['id'],))
        available_spot = curr.fetchone()
        lot_dict['available_spot_number'] = available_spot['spot_number'] if available_spot else None
        available_slot_data.append(lot_dict)
        
    conn.close()
    conn=conn_database()
    curr=conn.cursor()
    curr.execute('''SELECT BD.price as paid_price,PS.lot_id as li,BD.spot_number as sn,BD.id as id,BD.vehicle_number as vn,BD.timestamp_booked as tb,PL.prime_location as pl,BD.timestamp_released as tr,PL.price as price,BD.booking_status as b_status
                 FROM BOOKING_DETAILS BD 
                 JOIN  PARKING_SPOT PS ON PS.spot_number=BD.spot_number AND PS.lot_id = BD.lot_id
                 JOIN  PARKING_LOT PL on PL.id=PS.lot_id WHERE BD.user_id=? ORDER BY BD.timestamp_booked DESC''',(session['id'],))
    booking_details = [dict(row) for row in curr.fetchall()]
    conn.close()
    return jsonify({"lots": available_slot_data, "history": booking_details}), 200


@user_view.route('/api/user/book', methods=['POST'])
@login_required
def book_lot():
    flag = True
    data = request.get_json()
    spot_number = data.get('spot_number')
    vehicle_number = data.get('vehicle_number')
    conn = conn_database()
    curr = conn.cursor()
    curr.execute('SELECT no_of_available FROM PARKING_LOT WHERE id =?',(data.get('lot_id'),))
    available = int(curr.fetchone()[0])
    if available < 1:
        conn.close()
        return jsonify({"message": "No Slots available"}), 400
    curr.execute('INSERT INTO BOOKING_DETAILS (user_id,lot_id,spot_number,timestamp_booked,vehicle_number,booking_status) VALUES(?,?,?,?,?,?)',(session['id'],data.get('lot_id'),data.get('spot_number'),int(datetime.now().timestamp()),data.get('vehicle_number'),"open"))
    conn.commit()
    curr.execute('UPDATE PARKING_SPOT SET status ="O" WHERE lot_id = ? AND spot_number=?',(data.get('lot_id'),data.get('spot_number')))
    curr.execute('UPDATE PARKING_LOT SET no_of_available=no_of_available-1 where id=?',(data.get('lot_id'),))
    conn.commit()
    conn.close()
    return jsonify({"message": "Booking Successful"}), 200

@user_view.route('/api/user/release', methods=['POST'])
@login_required
def release_spot():
    data = request.get_json()
    lot_id = data.get('lot_id')
    spot_number = data.get('spot_number')
    booking_id = data.get('booking_id')

    conn = conn_database()
    curr = conn.cursor()

    curr.execute('''
        SELECT BD.timestamp_booked, PL.price as hourly_rate 
        FROM BOOKING_DETAILS BD
        JOIN PARKING_LOT PL ON BD.lot_id = PL.id
        WHERE BD.id = ?
    ''', (booking_id,))
    record = curr.fetchone()
    
    if not record:
        conn.close()
        return jsonify({"message": "Booking not found"}), 404
    
    start_time = record[0]
    rate = record[1]
    end_time = int(datetime.now().timestamp())
    
    duration_hours = (end_time - start_time) / 3600
    total_cost = round(duration_hours * rate, 2)

    curr.execute('UPDATE BOOKING_DETAILS SET booking_status=?, timestamp_released=?, price=? WHERE id=?', 
                 ("closed", end_time, total_cost, booking_id))
    
    curr.execute('UPDATE PARKING_SPOT SET status=? WHERE lot_id=? AND spot_number=?', 
                 ('A', lot_id, spot_number))
    
    curr.execute('UPDATE PARKING_LOT SET no_of_available=no_of_available+1 WHERE id=?', (lot_id,))
    
    conn.commit()
    conn.close()
    return jsonify({"message": f"Spot Released. Total Cost: ₹{total_cost}"}), 200




@user_view.route('/api/user/summary', methods=['GET'])
@login_required
def user_summary():

    user_id = session['id']
    conn = conn_database()
    curr = conn.cursor()

    curr.execute("SELECT * FROM USERS WHERE id=?", (session['id'],))
    user = curr.fetchone()

    stats = {}
    curr.execute("SELECT COUNT(*) FROM BOOKING_DETAILS WHERE user_id=?", (user_id,))
    stats['total'] = curr.fetchone()[0]

    curr.execute("SELECT COUNT(*) FROM BOOKING_DETAILS WHERE user_id=? AND booking_status='open'", (session['id'],))
    stats['active'] = curr.fetchone()[0]

    curr.execute("SELECT SUM(price) FROM BOOKING_DETAILS WHERE user_id=? AND booking_status='closed'", (session['id'],))
    stats['spent'] = curr.fetchone()[0] or 0

    curr.execute('''SELECT B.*, P.lot_id 
                    FROM BOOKING_DETAILS B 
                    JOIN PARKING_SPOT P ON B.spot_number = P.spot_number AND B.lot_id=P.lot_id
                    WHERE B.user_id=?
                    ORDER BY B.timestamp_booked DESC 
                    LIMIT 10''', (session['id'],))
    recent_bookings = curr.fetchall()

    return jsonify({"user": user, "stats": stats}), 200


@user_view.route('/api/user/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    conn = conn_database()
    curr = conn.cursor()

    curr.execute('SELECT * FROM USERS WHERE email =?',(session['email'],))
    user = curr.fetchone()
    id = user['id']
    conn.close()

    if request.method == 'POST':
        data = request.get_json()
        curr.execute('UPDATE USERS SET name=?, address=?, pincode=? WHERE id=?', 
                     (data['name'], data['address'], data['pincode'], session['id']))
        conn.commit()
        conn.close()
        return jsonify({"message": "Profile Updated"}), 200
    return jsonify(user), 200


@user_view.route('/logout')
@login_required
def user_logout():
    session.clear()
    return jsonify({"message": "Logged out",}), 200
    

from flask import Blueprint, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from .__init__ import conn_database


u_view = Blueprint('base',__name__)



@u_view.route('/')
def index():
    return jsonify({"message": "API Running"}), 200


@u_view.route('/register', methods=['POST'])
def user_register():
    name = request.form.get('user_name')
    email = request.form.get('user_email')
    password = request.form.get('user_password')
    confirm_password = request.form.get('user_confirm_password')
    
    if not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    if password != confirm_password:
        return jsonify({"message": "Passwords do not match"}), 400
        
    conn = conn_database()
    curr = conn.cursor()

    
    curr.execute('SELECT id from users WHERE email = ?',(email,))
    existing_user = curr.fetchone()

    if existing_user:
        conn.close()
        return jsonify({"message": "Email already registered"}), 409
    
    curr.execute('INSERT INTO USERS (name,email,password) VALUES (?,?,?)',(name,email,generate_password_hash(password)))
    conn.commit()
    conn.close()
    return jsonify({"message": "Registration Successful"}), 201

@u_view.route('/login',methods=['POST'])
def user_login():
    email = request.form.get('user_email')
    password = request.form.get('user_password')
    conn = conn_database()
    curr = conn.cursor()
    curr.execute('SELECT * FROM USERS WHERE email=?',(email,))
    user=curr.fetchone()
    conn.close()

    #Add check for wrong password or no user

    if user and check_password_hash(user['password'],password):
        session['id'] = user['id']
        session['email'] = user['email']
        session['is_admin'] = bool(user['is_admin'])

        role = 'admin' if bool(user['is_admin']) else 'user'
        return jsonify({"message": "Login Success", "role": role}), 200
            
    else:
        return jsonify({"message": "Incorrect Email or Password"}), 401


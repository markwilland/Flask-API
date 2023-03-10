import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)

app.config["DEBUG"] = True

def check_api_key():
    api_key = request.headers.get('api_key')
    
    if not api_key:
        return False, {'error': 'No API Key provided in the header!'}
    
    conn = sqlite3.connect('referrals.db')    
    cur = conn.cursor()
    cur.execute('SELECT * FROM api_keys WHERE key=?', (api_key,))
    
    key_data = cur.fetchone()
    conn.close()
    
    if key_data:
        return True, None
    else:
        return False, {'error': 'Invalid API Key'}

def dict_factory(cursor, row):
    d = {}

    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]

    return d


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/api/v1/resources/referrals/all', methods=['GET'])
def get_all_referrals():
    conn = sqlite3.connect('referrals.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    referrals = cur.execute('SELECT * FROM referrals;').fetchall()

    return jsonify(referrals)


@app.route('/api/v1/resources/referrals/<int:referral_id>', methods=['GET'])
def get_referral_by_id(referral_id):
    print("Referal Id Provided: " + str(referral_id))

    if referral_id is None or referral_id == 0:
        return jsonify({'message': 'Error: No id field provided. Please specify an id.'}), 400

    conn = sqlite3.connect('referrals.db')
    cur = conn.cursor()

    select_sql = '''SELECT * FROM referrals WHERE id = ?'''

    cur.execute(select_sql, (referral_id,))

    referral = cur.fetchone()

    conn.close()

    if referral is None:
        return jsonify({'message': f'Referral with Id {referral_id} not found'}), 404

    referral_dict = {
        'id': referral[0],
        'firm_code': referral[1],
        'file_type': referral[2],
        'name': referral[3],
        'email': referral[4],
        'phone': referral[5],
        'street_address_1': referral[6],
        'street_address_2': referral[7],
        'city': referral[8],
        'province': referral[9],
        'postal_code': referral[10]
    }

    return jsonify({'message': 'Referral found', 'referral': referral_dict})


@app.route('/api/v1/resources/referrals', methods=['POST'])
def api_new():
    print(f'api key found?: {check_api_key()[0]} +    error message:  + {check_api_key()[1]}')
    
    if check_api_key()[0] == False:
        return jsonify(check_api_key()[1])
    
    print("Post Request Incoming")
    data = request.get_json()
    print(data)

    conn = sqlite3.connect('referrals.db')
    cur = conn.cursor()

    insert_statement = """
                INSERT INTO referrals (firm_code, file_type, name, email, phone, street_address_1, street_address_2, city, province, postal_code)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    insert_data = (
        data['firm_code'],
        data['file_type'],
        data['name'],
        data['email'],
        data['phone'],
        data['street_address_1'],
        data['street_address_2'],
        data['city'],
        data['province'],
        data['postal_code']
    )
    print(insert_data)

    cur.execute(insert_statement, insert_data)

    referral_id = cur.lastrowid

    print(referral_id)

    conn.commit()
    conn.close()

    print("Record inserted")

    return jsonify({'message': 'Referral added successfully!', 'referral_id': referral_id})

app.run()
from flask import Flask, jsonify
import pymysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

conn = pymysql.connect(
    host='your-rds-endpoint',
    user='admin',
    password='admin1234',
    db='studentdb'
)

@app.route('/students', methods=['GET'])
def get_students():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM students")
        data = cursor.fetchall()
    return jsonify(data)

app.run(host='0.0.0.0', port=80)

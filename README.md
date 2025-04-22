
# S3 Web Application

A simple guide on how to host a web application on **Amazon S3**, with a **PostgreSQL RDS database** and **Python Flask backend** on EC2.

## PART 1: Set up RDS (PostgreSQL)

1. Go to **RDS > Create Database**
2. Select engine: **PostgreSQL**
3. Use **Free Tier** template
4. Set credentials:
    **Username:** `admin`
    **Password:** `admin1234`
5. DB Name: `studentdb`
6. Enable **Public Access**: Yes
7. Click **Create Database**

### Update Security Group

Add an **inbound rule** to the RDS security group:

- **Type:** PostgreSQL
- **Source:** EC2 Security Group (or `0.0.0.0/0` for testing)

### Connect to RDS & Create Table

Use terminal or DBeaver to run:

```sql
CREATE TABLE students (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100)
);

INSERT INTO students (name) VALUES
('Alice'),
('Bob'),
('Charlie');
```

## PART 2: Set up EC2 Python Backend

1. Launch an EC2 instance (**Ubuntu**)
2. Install Python and Flask:

```bash
sudo yum update -y
sudo yum install python3 -y
pip3 install flask pymysql flask-cors
```

### Create `app.py`

```python
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
```

### Run the App

```bash
sudo python3 app.py
```

Test in browser:

```
http://<EC2-IP>/students
```

## PART 3: Create Frontend Website in S3

### Sample `index.html`

```html
<!DOCTYPE html>
<html>
<head>
  <title>Student List</title>
</head>
<body>
  <h1>Students</h1>
  <ul id="list"></ul>

  <script>
    fetch("http://<EC2-IP>/students")
      .then(res => res.json())
      .then(data => {
        const list = document.getElementById("list");
        data.forEach(row => {
          const li = document.createElement("li");
          li.textContent = row[1];
          list.appendChild(li);
        });
      });
  </script>
</body>
</html>
```

### Deploy to S3

1. Upload `index.html` to your S3 bucket
2. Enable **Static Website Hosting**
3. Make the bucket **public**
4. Add **public read policy** to the bucket
5. Open your **S3 website endpoint** — you should see the list of students fetched from RDS.

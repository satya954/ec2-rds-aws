from flask import Flask, jsonify, request, render_template_string, send_from_directory
import mysql.connector
import os

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"]
    )


@app.route("/health")
def health():
    try:
        conn = get_db_connection()
        conn.close()

        return jsonify({
            "status": "UP",
            "database": "CONNECTED"
        })

    except Exception as e:
        return jsonify({
            "status": "DOWN",
            "database": "DISCONNECTED",
            "error": str(e)
        }), 500


HOME_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="/favicon.ico" type="image/x-icon">
    <title>Employee Management API</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #f4f6f9; color: #333; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { max-width: 600px; width: 100%; background: #fff; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); padding: 40px; }
        h1 { font-size: 1.8rem; margin-bottom: 8px; }
        p { color: #666; margin-bottom: 24px; }
        h2 { font-size: 1rem; margin-bottom: 12px; color: #444; }
        .endpoint { background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px; margin-bottom: 12px; text-decoration: none; color: inherit; display: block; transition: box-shadow 0.2s; }
        .endpoint:hover { box-shadow: 0 2px 12px rgba(0,0,0,0.12); }
        .method { display: inline-block; font-weight: 700; font-size: 0.8rem; padding: 2px 8px; border-radius: 4px; margin-right: 8px; }
        .get { background: #d1fae5; color: #065f46; }
        .post { background: #dbeafe; color: #1e40af; }
        .health { background: #fef3c7; color: #92400e; }
        code { font-size: 0.9rem; background: #e5e7eb; padding: 2px 6px; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Employee Management API</h1>
        <p>A simple REST API for managing employee records.</p>

        <h2>Available Endpoints</h2>

        <a class="endpoint" href="/health">
            <span class="method health">GET</span>
            <code>/health</code>
            <p style="margin-top:8px; margin-bottom:0;">Check API and database health status.</p>
        </a>

        <a class="endpoint" href="/employees">
            <span class="method get">GET</span>
            <code>/employees</code>
            <p style="margin-top:8px; margin-bottom:0;">Get all employees.</p>
        </a>

        <div class="endpoint">
            <span class="method post">POST</span>
            <code>/employees</code>
            <p style="margin-top:8px; margin-bottom:0;">Create a new employee. Send JSON with <code>name</code> and <code>department</code>.</p>
        </div>
    </div>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HOME_PAGE)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "favicon.ico")


@app.route("/employees", methods=["GET"])
def employees():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, name, department FROM employees"
    )

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(data)


@app.route("/employees", methods=["POST"])
def create_employee():

    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO employees (name, department)
        VALUES (%s, %s)
        """,
        (
            data["name"],
            data["department"]
        )
    )

    conn.commit()

    employee_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({
        "id": employee_id,
        "message": "Employee created"
    }), 201


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )

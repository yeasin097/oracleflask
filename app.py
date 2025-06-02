from flask import Flask, request, render_template
import cx_Oracle
import os

app = Flask(__name__)

# Database connection (vulnerable, using environment variables)
def get_db_connection():
    dsn = cx_Oracle.makedsn(
        os.getenv("ORACLE_HOST", "oracle"),
        os.getenv("ORACLE_PORT", 1521),
        service_name=os.getenv("ORACLE_SERVICE", "ORCL")
    )
    connection = cx_Oracle.connect(
        user=os.getenv("ORACLE_USER", "sys"),
        password=os.getenv("ORACLE_PASSWORD", "oracle"),
        dsn=dsn,
        mode=cx_Oracle.SYSDBA
    )
    return connection

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Vulnerable SQL query (no parameterization)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        
        if result:
            return render_template('result.html', message="Login successful!", data=result)
        else:
            return render_template('result.html', message="Login failed. Invalid credentials.")
    except cx_Oracle.DatabaseError as e:
        return render_template('result.html', message=f"Database error: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
import psycopg2

try:
    conn = psycopg2.connect("dbname=supplier_compliance_db user=postgres password='your_password' host=localhost")
    print("Connected successfully!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)

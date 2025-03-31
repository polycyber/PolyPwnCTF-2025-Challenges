from flask import Flask, request, abort
import psycopg2
import string

app = Flask(__name__)
ALLOWED_IPS = [
    "172.18.0.73",
]

from ipaddress import ip_address, ip_network

def is_allowed_ip(ip):
    """Check if an IP is in the allowed range."""
    for allowed_ip in ALLOWED_IPS:
        if ip_address(ip) in ip_network(allowed_ip, strict=False):
            return True
    return False

@app.before_request
def limit_remote_addr():
    client_ip = request.remote_addr
    if not is_allowed_ip(client_ip):
        abort(403)  # Forbidden

# Database connection details
DB_HOST = "sqlite"  # Change to your PostgreSQL host
DB_NAME = "strangedb"     # Change to your database name
DB_USER = "postgres"   # Change to your database username
DB_PASS = "stephen89701"   # Change to your database password

def query_db(sql_query):
    """Execute a raw SQL query (vulnerable to SQL injection)."""
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    cur = conn.cursor()
    cur.execute(sql_query)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

def rot18(text):
    def shift_char(c):
        if 'a' <= c <= 'z':
            return chr(((ord(c) - ord('a') + 18) % 26) + ord('a'))
        elif 'A' <= c <= 'Z':
            return chr(((ord(c) - ord('A') + 18) % 26) + ord('A'))
        return c  # Leave non-alphabet characters unchanged

    return ''.join(shift_char(c) for c in text)

@app.route('/mfanwjkwk', methods=['GET'])
def vulnerable_query():
    apitoken: str = request.headers.get("X-Token")
    xlimit: str = request.headers.get("X-Limit")
    if not apitoken:
        return "Missing X-Token header", 401
    if apitoken != "lgcwfsha":
        return "Unauthorized", 401
    if not xlimit:
        return "Missing X-Limit header", 400
    xlimit: str = rot18(xlimit)
    if "drop" in xlimit.lower() or "exec" in xlimit.lower():
        return "Multiverse does not like bad people. Fancy a cup of tea?", 418
    if "SELECT" in xlimit or "select" in xlimit:
        return "We banned the select keyword with our super powerful multiverse filter technology. What you gonna do about it?", 400
    sql = "SELECT * FROM universes LIMIT " + xlimit + ";"

    try:
        result = query_db(sql)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

from flask import Flask, request, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'testdb'

mysql = MySQL()
mysql.init_app(app)

@app.route('/add-user', methods=['POST'])
def add_user():
    data = request.json
    name = data['name']
    email = data['email']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        (name, email)
    )
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "User added successfully"})

@app.route('/users', methods=['GET'])
def get_users():
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email FROM users")
    rows = cursor.fetchall()

    users = []
    for row in rows:
        users.append({
            "id": row[0],
            "name": row[1],
            "email": row[2]
        })

    cursor.close()
    conn.close()

    return jsonify(users)

@app.route('/update-user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    name = data['name']
    email = data['email']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET name=%s, email=%s WHERE id=%s",
        (name, email, user_id)
    )
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "User updated successfully"})

@app.route('/delete-user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "User deleted successfully"})

print(app.url_map)

if __name__ == '__main__':
    app.run(debug=True)

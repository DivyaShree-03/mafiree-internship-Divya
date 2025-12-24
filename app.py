from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
import os
print("RUNNING FILE:", os.path.abspath(__file__))

app = Flask(__name__)


app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'testdb'

mysql = MySQL()
mysql.init_app(app)

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
    """
     cursor.execute(
        "DELETE FROM users WHERE id=%s",
        (user_id,)
     ) """
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Updated successfully"})
print(app.url_map)
if __name__ == '__main__':
    app.run(debug=True)



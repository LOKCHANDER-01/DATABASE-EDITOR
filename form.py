from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_users_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            phone_number TEXT NOT NULL,
            address TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


@app.before_first_request
def initialize():
    create_users_table()


@app.route('/')
def front():
    return render_template('front.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']
    phone_number = request.form['phone_number']
    address = request.form['address']

    conn = get_db_connection()
    conn.execute('INSERT INTO users (name, age, phone_number, address) VALUES (?, ?, ?, ?)',
                 (name, age, phone_number, address))
    conn.commit()
    conn.close()
    return redirect(url_for('field'))


@app.route('/field')
def field():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('field.html', database=users)


@app.route('/change/<int:id>', methods=['GET', 'POST'])
def change(id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        phone_number = request.form['phone_number']
        address = request.form['address']

        conn.execute('UPDATE users SET name = ?, age = ?, phone_number = ?, address = ? WHERE id = ?',
                     (name, age, phone_number, address, id))
        conn.commit()
        conn.close()
        return redirect(url_for('field'))

    conn.close()
    return render_template('change.html', user=user)


@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('field'))


if __name__ == '__main__':
    app.run(debug=True)

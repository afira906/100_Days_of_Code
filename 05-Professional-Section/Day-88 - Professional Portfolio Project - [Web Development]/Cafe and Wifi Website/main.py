from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['DATABASE'] = os.path.join(app.instance_path, 'cafes.db')


def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with app.app_context():
        conn = get_db_connection()
        # Check if table exists, if not create it
        conn.execute('''
            CREATE TABLE IF NOT EXISTS cafe (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                map_url TEXT,
                img_url TEXT,
                location TEXT,
                seats TEXT,
                has_toilet BOOLEAN,
                has_wifi BOOLEAN,
                has_sockets BOOLEAN,
                can_take_calls BOOLEAN,
                coffee_price TEXT
            )
        ''')
        conn.commit()
        conn.close()


@app.route('/')
def index():
    conn = get_db_connection()
    cafes = conn.execute('SELECT * FROM cafe').fetchall()
    conn.close()
    return render_template('index.html', cafes=cafes)


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    if request.method == 'POST':
        name = request.form['name']
        map_url = request.form['map_url']
        img_url = request.form['img_url']
        location = request.form['location']
        seats = request.form['seats']
        has_toilet = 'has_toilet' in request.form
        has_wifi = 'has_wifi' in request.form
        has_sockets = 'has_sockets' in request.form
        can_take_calls = 'can_take_calls' in request.form
        coffee_price = request.form['coffee_price']

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO cafe (name, map_url, img_url, location, seats, has_toilet, has_wifi, has_sockets, can_take_calls, coffee_price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, map_url, img_url, location, seats, has_toilet, has_wifi, has_sockets, can_take_calls, coffee_price))
        conn.commit()
        conn.close()

        flash('Cafe added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:cafe_id>')
def delete_cafe(cafe_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM cafe WHERE id = ?', (cafe_id,))
    conn.commit()
    conn.close()

    flash('Cafe deleted successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/api/cafes')
def api_cafes():
    conn = get_db_connection()
    cafes = conn.execute('SELECT * FROM cafe').fetchall()
    conn.close()

    cafes_list = []
    for cafe in cafes:
        cafes_list.append({
            'id': cafe['id'],
            'name': cafe['name'],
            'map_url': cafe['map_url'],
            'img_url': cafe['img_url'],
            'location': cafe['location'],
            'seats': cafe['seats'],
            'has_toilet': bool(cafe['has_toilet']),
            'has_wifi': bool(cafe['has_wifi']),
            'has_sockets': bool(cafe['has_sockets']),
            'can_take_calls': bool(cafe['can_take_calls']),
            'coffee_price': cafe['coffee_price']
        })

    return jsonify(cafes_list)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)

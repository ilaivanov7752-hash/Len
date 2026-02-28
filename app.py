from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'мой_секретный_пароль_123'

# Главная страница с твоей формой
@app.route('/')
def index():
    return render_template('index.html')

# Обработчик, который ты написал
@app.route('/send', methods=['POST'])
def handle_form():
    # 1. Распаковка "чемодана"
    name = request.form.get('user_name')
    email = request.form.get('user_email')

    # 2. Работа с базой
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    # Создаем таблицу
    cursor.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT)')
    
    # Кладем данные в "столбики"
    cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    
    conn.commit()
    conn.close()

    flash(f"Спасибо, {name}! Данные успешно сохранены.")
    return redirect(url_for('index')) 


@app.route('/admin')
def admin_panel():
    conn = sqlite3.connect('test.db')
    # ВОТ ЭТА СТРОЧКА:
    conn.row_factory = sqlite3.Row 
    
    cursor = conn.cursor()
    cursor.execute('SELECT name, email FROM users')
    all_users = cursor.fetchall()
    conn.close()
    
    return render_template('admin.html', users=all_users)

# Та самая "запускалка"
if __name__ == '__main__':
    app.run(debug=True)

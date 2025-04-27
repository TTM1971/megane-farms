from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from blockchain import Blockchain
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'ta_cle_secrete_super_secrete'  # Important pour la sécurité

# Initialiser la Blockchain
food_chain = Blockchain()

# Initialiser Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Classe User pour Flask-Login
class User(UserMixin):
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

# Charger un utilisateur
@login_manager.user_loader
def load_user(user_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT id, username, password, role FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    connection.close()
    if user_data:
        return User(*user_data)
    return None

# Créer la base de données SQLite s'il n'y a pas encore
def init_db():
    if not os.path.exists('database.db'):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        connection.commit()
        connection.close()

# Appeler init_db au démarrage
init_db()

# Route inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']  # Personnel ou Client

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            connection.commit()
            flash('Compte créé avec succès, veuillez vous connecter.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Ce nom d’utilisateur est déjà utilisé.')
            return redirect(url_for('register'))
        finally:
            connection.close()

    return render_template('register.html')
if __name__ == "__main__":
    app.run(debug=True)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT id, username, password, role FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        connection.close()

        if user_data and user_data[2] == password:
            user = User(*user_data)
            login_user(user)
            flash('Connexion réussie.')
            if user.role == "Personnel":
                return redirect(url_for('dashboard_personnel'))
            else:
                return redirect(url_for('dashboard_client'))
        else:
            flash('Identifiant ou mot de passe incorrect.')
            return redirect(url_for('login'))

    return render_template('login.html')

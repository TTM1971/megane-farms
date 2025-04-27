from block import Block
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
#from blockchain import Blockchain
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'ta_cle_secrete_super_secrete'  # Important pour la sécurité

# Initialiser la Blockchain
food_chain = Bblock()

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

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", "Début de la traçabilité", "Origine", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, product_id, event, location):
        latest_block = self.get_latest_block()
        new_block = Block(
            index=latest_block.index + 1,
            product_id=product_id,
            event=event,
            location=location,
            previous_hash=latest_block.hash
        )
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            previous_block = self.chain[i - 1]
            current_block = self.chain[i]

            if current_block.hash != current_block.calculate_hash():
                print(f"Erreur de hash au bloc {current_block.index}")
                return False

            if current_block.previous_hash != previous_block.hash:
                print(f"Erreur de chaînage entre bloc {previous_block.index} et {current_block.index}")
                return False

        return True

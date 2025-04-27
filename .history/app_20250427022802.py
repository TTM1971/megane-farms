from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from blockchain import Blockchain
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
import re 

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
        role = request.form['role']

        # Vérifier la longueur du mot de passe
        if len(password) < 8:
            flash('Le mot de passe doit contenir au moins 8 caractères.', 'error')
            return redirect(url_for('register'))

        # Vérifier la présence d'au moins une majuscule
        if not re.search(r'[A-Z]', password):
            flash('Le mot de passe doit contenir au moins une lettre majuscule.', 'error')
            return redirect(url_for('register'))

        # Vérifier la présence d'au moins un chiffre
        if not re.search(r'\d', password):
            flash('Le mot de passe doit contenir au moins un chiffre.', 'error')
            return redirect(url_for('register'))

        # Hachage du mot de passe
        hashed_password = generate_password_hash(password)

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                           (username, hashed_password, role))
            connection.commit()
            flash('Compte créé avec succès, veuillez vous connecter.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Ce nom d’utilisateur est déjà utilisé.')
            return redirect(url_for('register'))
        finally:
            connection.close()

    return render_template('register.html')

    
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

        if user_data and check_password_hash(user_data[2], password):
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


# Tableau de bord pour le Personnel
@app.route('/dashboard_personnel', methods=['GET', 'POST'])
@login_required
def dashboard_personnel():
    if current_user.role != "Personnel":
        flash("Accès refusé.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        product_id = request.form['product_id']
        event = request.form['event']
        location = request.form['location']

        food_chain.add_block(product_id, event, location)
        flash('Produit ajouté à la blockchain avec succès.')

    # Envoyer toute la blockchain sauf le bloc Genesis (index 0)
    products = food_chain.chain[1:]  # On enlève le tout premier bloc ("Début de la traçabilité")
    return render_template('dashboard_personnel.html', username=current_user.username, products=products)

# Tableau de bord pour le Client
@app.route('/dashboard_client', methods=['GET', 'POST'])
@login_required
def dashboard_client():
    if current_user.role != "Client":
        flash("Accès refusé.")
        return redirect(url_for('login'))

    history = []
    if request.method == 'POST':
        product_id = request.form['product_id']

        # Chercher tous les blocs liés à ce produit
        history = [block for block in food_chain.chain if block.product_id == product_id]

    return render_template('dashboard_client.html', username=current_user.username, history=history)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Vous êtes déconnecté.")
    return redirect(url_for('login'))


@app.route('/')
def home():
    return render_template('home.html')









if __name__ == "__main__":
    app.run(debug=True)
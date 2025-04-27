from flask import Flask, render_template, request, redirect, url_for
from blockchain import Blockchain

app = Flask(__name__)
food_chain = Blockchain()

# Page d'accueil - choix du rôle
@app.route('/')
def index():
    return render_template('index.html')

# Page du personnel pour ajouter un événement
@app.route('/personnel')
def personnel():
    return render_template('personnel.html')

# Traitement du formulaire du personnel
@app.route('/ajouter', methods=['POST'])
def ajouter():
    product_id = request.form['product_id']
    event = request.form['event']
    location = request.form['location']
    food_chain.add_block(product_id, event, location)
    return redirect(url_for('personnel'))

# Page du client pour rechercher un produit
@app.route('/client')
def client():
    return render_template('client.html')

# Traitement de la recherche par client
@app.route('/chercher', methods=['POST'])
def chercher():
    product_id = request.form['product_id']
    produit_historique = []
    for block in food_chain.chain:
        if block.product_id == product_id:
            produit_historique.append(block)
    return render_template('historique.html', historique=produit_historique, product_id=product_id)

if __name__ == "__main__":
    app.run(debug=True)

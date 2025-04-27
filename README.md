# MeganeFarms
<img width="1115" alt="image" src="https://github.com/user-attachments/assets/bc37e927-206b-436a-b820-6ff83ba6119d" />

MeganeFarms est une application web de traçabilité des produits alimentaires, utilisant la blockchain pour assurer authenticité, sécurité et transparence.

## Présentation

MeganeFarms permet :
- Aux producteurs (personnel) d'enregistrer les étapes de vie des produits (récolte, transformation, stockage, transport, vente).
- Aux clients de vérifier facilement l'authenticité et l’historique d'un produit à l'aide de son identifiant.

Chaque événement est sécurisé dans une blockchain interne.

## Fonctionnalités principales

- Connexion sécurisée avec mots de passe hachés
- Enregistrement d’événements pour chaque produit
- Traçabilité complète de la production à la vente
- Vérification d’authenticité en temps réel pour les clients
- Interface utilisateur claire et moderne
- Affichage en frise chronologique des événements

## Technologies utilisées

- Python 3
- Flask
- SQLite
- Flask-Login
- HTML / CSS

## Installation et lancement

1. Cloner le projet

   git clone https://github.com/TTM1971/megane-farms.git
   cd megane-farms

2. Installer les dépendances

   pip install -r requirements.txt

3. Lancer l’application

   python app.py

Puis ouvrir votre navigateur à l'adresse suivante : http://127.0.0.1:5000

## Structure du projet

megane-farms/
├── app.py
├── blockchain.py
├── block.py
├── database.db (non inclus dans Git)
├── requirements.txt
├── README.md
├── .gitignore
├── static/
│   └── style.css
└── templates/
    ├── home.html
    ├── login.html
    ├── register.html
    ├── dashboard_personnel.html
    └── dashboard_client.html

## Aperçu

(Cette section peut contenir ultérieurement des captures d'écran de l'interface utilisateur.)

## Evolutions prévues

- Intégration de QR Codes pour l'identification des produits
- Renforcement de la validation des mots de passe
- Optimisation de l'affichage pour les mobiles
- Déploiement sur une infrastructure cloud

## Auteur

Projet développé par Tresor Megane  
Contact : tambattresor@icloud.com


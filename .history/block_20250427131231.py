import hashlib
import time

class Block:
    def __init__(self, index, name, title, node, product_id, event, location, previous_hash, timestamp=None, nonce=0):
        self.index = index
        self.name = name  # Nouveau : nom de la personne
        self.title = title  # Nouveau : titre de l'action
        self.node = node  # Nouveau : type de nœud (Ferme, Usine...)
        self.product_id = product_id  # ID du produit
        self.event = event  # Événement (récolte, etc.)
        self.location = location  # Lieu exact
        self.timestamp = timestamp if timestamp else time.time()
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        content = f"{self.index}{self.name}{self.title}{self.node}{self.product_id}{self.event}{self.location}{self.timestamp}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(content.encode()).hexdigest()

    def mine_block(self, difficulty):
        # difficulté = nombre de zéros demandés au début du hash
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

import hashlib
import time

class Block:
    def __init__(self, index, product_id, event, location, previous_hash, timestamp=None, nonce=0):
        self.index = index
        self.product_id = product_id
        self.event = event
        self.location = location
        self.timestamp = timestamp if timestamp else time.time()
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        content = f"{self.index}{self.product_id}{self.event}{self.location}{self.timestamp}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(content.encode()).hexdigest()

    def mine_block(self, difficulty):
        # difficulté = nombre de zéros demandés au début du hash
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

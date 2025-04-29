import hashlib
import time

class Block:
    def __init__(self, index, name, title, node, product_id, event, location, previous_hash, timestamp=None, nonce=0):
        self.index = index
        self.name = name
        self.title = title
        self.node = node
        self.product_id = product_id
        self.event = event
        self.location = location
        self.timestamp = timestamp if timestamp else time.time()
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        content = f"{self.index}{self.name}{self.title}{self.node}{self.product_id}{self.event}{self.location}{self.timestamp}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(content.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
def get_formatted_date(self):
    from datetime import datetime
    return datetime.fromtimestamp(self.timestamp).strftime("%d %B %Y à %Hh%M")

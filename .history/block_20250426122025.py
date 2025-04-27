import hashlib
import time

class Block:
    def __init__(self, index, product_id, event, location, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.product_id = product_id
        self.event = event
        self.location = location
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        content = (
            str(self.index) +
            str(self.timestamp) +
            str(self.product_id) +
            str(self.event) +
            str(self.location) +
            str(self.previous_hash)
        )
        return hashlib.sha256(content.encode()).hexdigest()

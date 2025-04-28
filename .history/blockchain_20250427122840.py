from block import Block
import json
import os
from datetime import datetime

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2  # Définir une difficulté (2 zéros à trouver)

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
        new_block.mine_block(self.difficulty)
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

    def save_to_file(self):
        chain_data = []
        for block in self.chain:
            block_data = {
                "index": block.index,
                "timestamp": block.timestamp,
                "product_id": block.product_id,
                "event": block.event,
                "location": block.location,
                "previous_hash": block.previous_hash,
                "hash": block.hash
            }
            chain_data.append(block_data)

        with open("blockchain_data.json", "w") as file:
            json.dump(chain_data, file, indent=4)

    def load_from_file(self):
        with open("blockchain_data.json", "r") as file:
            chain_data = json.load(file)
            self.chain = []
            for block_data in chain_data:
                block = Block(
                    index=block_data["index"],
                    product_id=block_data["product_id"],
                    event=block_data["event"],
                    location=block_data["location"],
                    previous_hash=block_data["previous_hash"]
                )
                block.timestamp = block_data["timestamp"]
                block.hash = block_data["hash"]
                self.chain.append(block)

class Block:
    def __init__(self, index, product_id, event, location, previous_hash):
        self.index = index
        self.timestamp = datetime.now().timestamp()  # Timestamp au moment de la création
        self.product_id = product_id
        self.event = event
        self.location = location
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        import hashlib
        data = f"{self.index}{self.timestamp}{self.product_id}{self.event}{self.location}{self.previous_hash}"
        return hashlib.sha256(data.encode()).hexdigest()

    def get_formatted_date(self):
        return datetime.fromtimestamp(self.timestamp).strftime("%d %B %Y à %Hh%M")

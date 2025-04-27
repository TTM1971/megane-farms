import json
import os
from block import Block

class Blockchain:
    def __init__(self):
        self.chain = []
        if os.path.exists("blockchain_data.json"):
            self.load_from_file()
        else:
            self.chain = [self.create_genesis_block()]
            self.save_to_file()

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
        self.save_to_file()

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

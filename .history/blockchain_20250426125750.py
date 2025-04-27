from block import Block

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

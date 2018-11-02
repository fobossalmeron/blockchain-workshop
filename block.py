import hashlib as hl
import json

ledger = {"Rodrigo": 100, "Gina": 100, "Shrey": 100}
miner = "Rodrigo"


class BlockChain:
    genesis_block = {'previous_hash': '', 'index': 0, 'transactions': []}
    mining_reward = 10
    open_transactions = []
    corrupt_chain = False

    def __init__(self):
        self.chain = []
        self.chain.append(self.genesis_block)

    def hack_block(self, block):
        self.chain[block] = "HACK DANGER"

    def encrypt(self, block):
        ash = hl.sha256(
            json.dumps(block).encode()).hexdigest()
        return ash

    def add_transaction_to_list(self, transaction):
        self.check_integrity()
        if transaction.is_valid() and not self.corrupt_chain:
            self.open_transactions.append(transaction)
        else:
            print("\nYour transaction is invalid, the blockchain was altered")

    def push_transactions_to_ledger(self):
        for transaction in self.open_transactions:
            if transaction.sender == "reward":
                ledger[transaction.recipient] = float(
                    ledger[transaction.recipient]) + float(transaction.amount)
            else:
                print(transaction.sender, "sends",
                      transaction.amount, "to", transaction.recipient)
                ledger[transaction.sender] = float(
                    ledger[transaction.sender]) - float(transaction.amount)
                ledger[transaction.recipient] = float(
                    ledger[transaction.recipient]) + float(transaction.amount)

    def check_integrity(self):
        for index, block in enumerate(self.chain):
            if index == 0:
                print(
                    "\nVerifyling integrity of the Blockchain\nChecking genesis block ...")
                if block == self.genesis_block:
                    print("Genesis block is ok")
                else:
                    print("Genesis block has been altered")
                    print("You cannot add new blocks, the chain has been altered")
                    self.corrupt_chain = True
                    return False
                previous_block = block
            else:
                print("Checking block", index, "...")
                if "previous_hash" in block and block["previous_hash"] == self.encrypt(previous_block):
                    print("Block", 1, "is ok")
                else:
                    print("Block", index, "has been altered")
                    print("\nYou cannot add new blocks, the chain has been altered\n")
                    return False
                previous_block = block
        print("Integrity of Blockchain verified\n")
        return True

    def output_transactions(self, transactions):
        output_transactions = []
        for pending_transaction in transactions:
            output_transactions.append(vars(pending_transaction))
        return output_transactions

    def mine_block(self, miner):
        if self.check_integrity():
            previous_block = self.chain[-1]
            previous_block_hash = hl.sha256(
                json.dumps(previous_block).encode()).hexdigest()

            transactions_output = self.output_transactions(
                self.open_transactions)

            self.chain.append({"previous_hash": previous_block_hash,
                               "index": (previous_block["index"] + 1),
                               "transactions": transactions_output})
            print("Mining done \nThe updated blockchain is", self.chain, "\n")
            self.push_transactions_to_ledger()
            print(ledger)

            # Prepare mining reward for next block
            self.open_transactions.clear()
            reward_transaction = Transaction(
                "reward", miner, self.mining_reward)
            self.open_transactions.append(reward_transaction)
            print("\nBlock successfully mined\n")
        else:
            print("\nBlock couldn't be mined")


class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = float(amount)

    def is_valid(self):
        is_valid = True
        while is_valid:
            if self.sender == "reward":
                if self.recipient in ledger:
                    is_valid = True
                    return is_valid
                else:
                    print("Miner is not registered")
                    is_valid = False
                    return is_valid
                return is_valid
            elif self.sender in ledger:
                is_valid = True
                if self.recipient in ledger:
                    is_valid = True
                    if ledger[self.sender] >= self.amount:
                        is_valid = True
                        return is_valid
                    else:
                        print(self.sender, "doesn't have sufficient funds\nHe was requested",
                              self.amount, "but only has", ledger[self.sender], "in the ledger")
                        is_valid = False
                else:
                    print("Recipient not in ledger")
                    is_valid = False
            else:
                print("Sender not in ledger")
                is_valid = False
        return is_valid

    def push_transaction(self):
        if self.sender == "reward":
            ledger[self.recipient] = float(
                ledger[self.recipient]) + float(self.amount)
        else:
            ledger[self.sender] = float(
                ledger[self.sender]) - float(self.amount)
            ledger[self.recipient] = float(
                ledger[self.recipient]) + float(self.amount)


def run_program():
    print("\n ----- Welcome to Blockchain")
    running = True
    blockchain = BlockChain()
    blockchain.add_transaction_to_list(Transaction("Gina", "Rodrigo", 50))
    blockchain.add_transaction_to_list(Transaction("Gina", "Rodrigo", 50))
    blockchain.mine_block(miner)
    while running:
        user_input = input("""\nPlease choose
1: Add a new transaction
2: Mine new block
3: Output all open transactions
4: Output all participants
5: Output the blockchain blocks
h: Manipulate the chain
q: Quit\n""")
        if user_input == "1":
            print("\nYou chose to add a new transaction\n")
            sender = input("Sender: \n")
            recipient = input("Recipient: \n")
            amount = float(input("Transaction amount: \n"))
            blockchain.add_transaction_to_list(
                Transaction(sender, recipient, amount))
            print("You added the transaction to the queue")
        elif user_input == "2":
            print("\nYou chose to mine a block.\nMining...")
            blockchain.mine_block(miner)
        elif user_input == "3":
            print("\nYou chose to display all open transactions\nThe current open transactions are:",
                  blockchain.output_transactions(blockchain.open_transactions), "\n")
        elif user_input == "4":
            print("\nYou chose to display all participants\n\nThe participants are:")
            for participant in ledger.keys():
                print(participant)
        elif user_input == "5":
            if blockchain.chain == blockchain.genesis_block:
                print("Blockchain still in genesis block\n")
            else:
                print("The blockchain is", blockchain.chain, "\n")
        elif user_input == "h":
            print("The blockchain currently is", blockchain.chain, "\n")
            chosen_block = int(input("\nWhich block do you want to alter?\n"))
            if chosen_block >= len(blockchain.chain):
                print("The index",chosen_block,"doesn't exist")
            else:
                blockchain.hack_block(chosen_block)
                print("The new blockchain is", blockchain.chain, "\n")
        elif user_input == "check":
            blockchain.check_integrity()
        elif user_input == "q":
            print("See you next time")
            running = False
        else:
            print("Command '", user_input, "' is invalid\n")

run_program()

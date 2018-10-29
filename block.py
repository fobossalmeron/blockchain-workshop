''' 
Extend your programme with the following:
- terminal user interface

    hack/edit the blockchain

implement a function that checks the integrity of the blockchain

'''

blockchain = []
genesis_block = ["x",0,"x","genesis"]

def init_blockchain():
    blockchain.append(genesis_block)

def edit_blockchain(newblockchain):
    print(newblockchain)
    print(blockchain)
    blockchain = newblockchain

def record_new_block(sender, amount, recipient):
    previous_block = blockchain[-1]
    blockchain.append([sender,amount,recipient,previous_block])

def run_program():
    running = True
    init_blockchain()
    while running:
        user_input = input("Choose your desired action: \n")
        if user_input == "q":
            print("See you next time")
            running = False
        elif user_input == "1":
            print("You chose new transaction \n")
            sender = input("Sender: \n")
            recipient = input("Recipient: \n")
            amount = input("Transaction amount: \n")
            record_new_block(sender, amount, recipient)
            print("Transaction done 3 times \nThe updated blockchain is",blockchain)
        elif user_input == "print":
            if blockchain == [genesis_block]:
                print("Blockchain still in genesis block")
            else:
                print("The blockchain is",blockchain)
        elif user_input == "hack":
                print("The blockchain currently is",blockchain)
                altered_chain = input("\nEnter new blockchain")
                edit_blockchain(altered_chain)
                print("The blockchain currently is",blockchain)

        else:
            print("Command '",user_input,"' is invalid")

run_program()


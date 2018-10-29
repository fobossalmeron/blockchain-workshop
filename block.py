''' 
Extend your programme with the following:
- terminal user interface

    hack/edit the blockchain

implement a function that checks the integrity of the blockchain

'''

blockchain = []
genesis_block = ["x",0,"x","genesis"]
bad_chain = False


def init_blockchain():
    blockchain.append(genesis_block)

def edit_blockchain(block):
    blockchain[block] = "pasto"

def record_new_block(sender, amount, recipient):
    if check_integrity():
        previous_block = blockchain[-1]
        blockchain.append([sender,amount,recipient,previous_block])
        print("Transaction done \nThe updated blockchain is",blockchain,"\n")
    else:
        print("You cannot add new blocks, the chain has been altered")

def check_integrity():
    for i, x in enumerate(blockchain):
        if i == 0:
            print ("checking genesis block")
            if x == genesis_block:
                print("genesis block is ok")
            else: 
                print("genesis block has been altered")
                return False
            previous_block = x
        else:
            print("checking block", i)
            if x[3] == previous_block:
                print("block", 1, "is ok")
            else:
                print("block", i, "has been altered")
                return False
            previous_block = x
    print("all blocks have been checked\n")
    return True

def enter_dummy_data():
    record_new_block("ro", 300, "gin")
    record_new_block("gin", 500, "ro")

def run_program():
    running = True
    init_blockchain()
    enter_dummy_data()
    while running:
        user_input = input("Please choose \n1: Add a new transaction\n2: Print the blockchain blocks\nh: Hack the chain\nq: Quit\n\nYour choice:\n\n")
        if user_input == "1":
            print("\nYou chose new transaction \n")
            sender = input("Sender: \n")
            recipient = input("Recipient: \n")
            amount = float(input("Transaction amount: \n"))
            record_new_block(sender, amount, recipient)
        elif user_input == "2":
            if blockchain == [genesis_block]:
                print("Blockchain still in genesis block\n")
            else:
                print("The blockchain is",blockchain,"\n")
        elif user_input == "h":
                print("The blockchain currently is",blockchain, "\n")
                chosen_block = int(input("\nWhich block do you want to alter?\n"))
                edit_blockchain(chosen_block)
                print("The new blockchain is",blockchain, "\n")
        elif user_input == "check":
            if check_integrity():
                print("all well with blockchain\n\n")
            else:
                print("blockchain was altered\n\n")
        elif user_input == "q":
            print("See you next time")
            running = False
        else:
            print("Command '",user_input,"' is invalid\n")

run_program()


import Crypto
import binascii
import datetime
import collections
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA


class Client:
    def __init__(self, initial_balance=0):
        random_generator = Crypto.Random.new().read
        self._private_key = RSA.generate(1024, random_generator)
        self._public_key = self._private_key.publickey()
        self._signer = PKCS1_v1_5.new(self._private_key)
        self.balance = initial_balance

    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')

    def __repr__(self):
        return f"Client(ID: {self.identity[:10]}..., Balance: {self.balance})"

    def sign_transaction(self, transaction_dict):
        private_key = self._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(transaction_dict).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')


class Transaction:
    def __init__(self, sender_client, receiver_identity, value):
        self.sender = sender_client
        self.receiver = receiver_identity
        self.value = value
        self.time = datetime.datetime.now()
        self.signature = None

    def to_dict(self):
        if isinstance(self.sender, str) and self.sender == "Genesis":
            sender_identity = "Genesis"
        else:
            sender_identity = self.sender.identity
        return collections.OrderedDict({
            'sender': sender_identity,
            'receiver': self.receiver,
            'value': self.value,
            'time': self.time
        })

    def sign(self):
        if isinstance(self.sender, str) and self.sender == "Genesis":
            self.signature = "Genesis Transaction - No Signature"
        else:
            self.signature = self.sender.sign_transaction(self.to_dict())

    def execute_transaction(self, all_clients):
        if isinstance(self.sender, str) and self.sender == "Genesis":
            receiver_client = all_clients.get(self.receiver)
            if receiver_client:
                receiver_client.balance += self.value
                return True
            return False

        if self.sender.balance >= self.value:
            self.sender.balance -= self.value
            receiver_client = all_clients.get(self.receiver)
            if receiver_client:
                receiver_client.balance += self.value
                return True
            else:
                print(f"Warning: Receiver {self.receiver} not found in client list.")
                return False
        else:
            print(f"Transaction failed: Sender {self.sender.identity[:10]}... has insufficient funds ({self.sender.balance} < {self.value})")
            return False


def display_transaction(transaction):
    transaction_dict = transaction.to_dict()
    print("Sender:", transaction_dict["sender"])
    print("-----")
    print("Receiver:", transaction_dict["receiver"])
    print("-----")
    print("Value:", str(transaction_dict["value"]))
    print("-----")
    print("Time:", str(transaction_dict["time"]))
    print("-----")
    print("Signature:", transaction.signature)
    print("-----")


# Demo
print("-" * 50)
print("Practical 1c: Transaction Class with Money Transfer Logic")
print("-" * 50)

alice = Client(initial_balance=100)
bob = Client(initial_balance=50)
charlie = Client(initial_balance=20)

all_clients = {
    alice.identity: alice,
    bob.identity: bob,
    charlie.identity: charlie
}

print("Initial Balances:")
for client_id, client_obj in all_clients.items():
    print(f"Client ID: {client_id[:10]}..., Balance: {client_obj.balance}")
print("-" * 50)

print("Performing Transactions:")

tx1 = Transaction(alice, bob.identity, 30)
tx1.sign()
print("\nTransaction 1 (Alice to Bob, 30):")
display_transaction(tx1)
if tx1.execute_transaction(all_clients):
    print("Transaction 1 successful.")
else:
    print("Transaction 1 failed.")

tx2 = Transaction(bob, charlie.identity, 20)
tx2.sign()
print("\nTransaction 2 (Bob to Charlie, 20):")
display_transaction(tx2)
if tx2.execute_transaction(all_clients):
    print("Transaction 2 successful.")
else:
    print("Transaction 2 failed.")

tx3 = Transaction(charlie, alice.identity, 100)
tx3.sign()
print("\nTransaction 3 (Charlie to Alice, 100 - Insufficient Funds):")
display_transaction(tx3)
if tx3.execute_transaction(all_clients):
    print("Transaction 3 successful.")
else:
    print("Transaction 3 failed due to insufficient funds.")

print("\n" + "-" * 50)
print("Final Balances:")
for client_id, client_obj in all_clients.items():
    print(f"Client ID: {client_id[:10]}..., Balance: {client_obj.balance}")
print("-" * 50)

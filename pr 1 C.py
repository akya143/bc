import binascii
import datetime
import collections

from Cryptodome import Random
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA


class Client:
    def __init__(self, initial_balance=0):
        # Random generator
        random_generator = Random.new().read

        # Generate keys
        self._private_key = RSA.generate(1024, random_generator)
        self._public_key = self._private_key.publickey()

        # Signer
        self._signer = PKCS1_v1_5.new(self._private_key)

        # Balance
        self.balance = initial_balance

    @property
    def identity(self):
        return binascii.hexlify(
            self._public_key.export_key(format='DER')
        ).decode('ascii')

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
        # Genesis transaction
        if isinstance(self.sender, str) and self.sender == "Genesis":
            receiver_client = all_clients.get(self.receiver)
            if receiver_client:
                receiver_client.balance += self.value
                return True
            return False

        # Check balance
        if self.sender.balance >= self.value:
            self.sender.balance -= self.value

            receiver_client = all_clients.get(self.receiver)
            if receiver_client:
                receiver_client.balance += self.value
                return True
            else:
                print("Receiver not found!")
                return False
        else:
            print(f"Transaction failed: Insufficient funds ({self.sender.balance} < {self.value})")
            return False


def display_transaction(transaction):
    transaction_dict = transaction.to_dict()

    print("Sender:", transaction_dict["sender"])
    print("-----")
    print("Receiver:", transaction_dict["receiver"])
    print("-----")
    print("Value:", transaction_dict["value"])
    print("-----")
    print("Time:", transaction_dict["time"])
    print("-----")
    print("Signature:", transaction.signature)
    print("-----")


# ---------------- DEMO ---------------- #

print("-" * 50)
print("Practical 1c: Transaction Class with Money Transfer Logic")
print("-" * 50)

# Create clients
alice = Client(initial_balance=100)
bob = Client(initial_balance=50)
charlie = Client(initial_balance=20)

# Store clients
all_clients = {
    alice.identity: alice,
    bob.identity: bob,
    charlie.identity: charlie
}

print("Initial Balances:")
for cid, client in all_clients.items():
    print(f"Client ID: {cid[:10]}..., Balance: {client.balance}")

print("-" * 50)

# Transaction 1
tx1 = Transaction(alice, bob.identity, 30)
tx1.sign()

print("\nTransaction 1 (Alice → Bob, 30):")
display_transaction(tx1)

if tx1.execute_transaction(all_clients):
    print("Transaction 1 successful.")
else:
    print("Transaction 1 failed.")

# Transaction 2
tx2 = Transaction(bob, charlie.identity, 20)
tx2.sign()

print("\nTransaction 2 (Bob → Charlie, 20):")
display_transaction(tx2)

if tx2.execute_transaction(all_clients):
    print("Transaction 2 successful.")
else:
    print("Transaction 2 failed.")

# Transaction 3 (Insufficient funds)
tx3 = Transaction(charlie, alice.identity, 100)
tx3.sign()

print("\nTransaction 3 (Charlie → Alice, 100):")
display_transaction(tx3)

if tx3.execute_transaction(all_clients):
    print("Transaction 3 successful.")
else:
    print("Transaction 3 failed due to insufficient funds.")

# Final balances
print("\n" + "-" * 50)
print("Final Balances:")

for cid, client in all_clients.items():
    print(f"Client ID: {cid[:10]}..., Balance: {client.balance}")

print("-" * 50)

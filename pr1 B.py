import binascii
import datetime
import collections

from Cryptodome import Random
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA


class Client:
    def __init__(self):
        # Creating random number generator for key generation
        random_generator = Random.new().read

        # Generating RSA private and public keys
        self._private_key = RSA.generate(1024, random_generator)
        self._public_key = self._private_key.publickey()

        # Initializing signer for digital signatures
        self._signer = PKCS1_v1_5.new(self._private_key)

    @property
    def identity(self):
        # Returns the public key in hexadecimal format
        return binascii.hexlify(
            self._public_key.export_key(format='DER')
        ).decode('ascii')


class Transaction:
    def __init__(self, sender, receiver, value):
        self.sender = sender
        self.receiver = receiver
        self.value = value
        self.time = datetime.datetime.now()

    def to_dict(self):
        # Convert transaction into OrderedDict
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.identity

        return collections.OrderedDict({
            'sender': identity,
            'receiver': self.receiver,
            'value': self.value,
            'time': self.time
        })

    def sign_transaction(self):
        # Sign the transaction
        if self.sender == "Genesis":
            return "Genesis Transaction - No Signature"

        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)

        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')


def display_transaction(transaction):
    """Display transaction details"""
    transaction_dict = transaction.to_dict()

    print("Sender:", transaction_dict["sender"])
    print("-----")
    print("Receiver:", transaction_dict["receiver"])
    print("-----")
    print("Value:", str(transaction_dict["value"]))
    print("-----")
    print("Time:", str(transaction_dict["time"]))
    print("-----")


# ---------------- DEMO ---------------- #

print("-" * 50)
print("Practical 1b: Creating and Displaying Multiple Transactions")
print("-" * 50)

# Create clients
ninad = Client()
ks = Client()
vighnesh = Client()
sairaj = Client()

print("Ninad's Key:", ninad.identity)
print("KS's Key:", ks.identity)
print("Vighnesh's Key:", vighnesh.identity)
print("Sairaj's Key:", sairaj.identity)

print("-" * 50)

# Transactions list
transactions = []

# Create transactions
t1 = Transaction(ninad, ks.identity, 15.0)
transactions.append(t1)

t2 = Transaction(ninad, vighnesh.identity, 6.0)
transactions.append(t2)

t3 = Transaction(ninad, sairaj.identity, 16.0)
transactions.append(t3)

t4 = Transaction(vighnesh, ninad.identity, 8.0)
transactions.append(t4)

t5 = Transaction(vighnesh, ks.identity, 19.0)
transactions.append(t5)

t6 = Transaction(vighnesh, sairaj.identity, 35.0)
transactions.append(t6)

t7 = Transaction(sairaj, vighnesh.identity, 5.0)
transactions.append(t7)

t8 = Transaction(sairaj, ninad.identity, 12.0)
transactions.append(t8)

t9 = Transaction(sairaj, ks.identity, 25.0)
transactions.append(t9)

t10 = Transaction(ninad, ks.identity, 1.0)
transactions.append(t10)

# Display transactions
print("Displaying all created transactions:")

for i, transaction in enumerate(transactions):
    print(f"\nTransaction {i+1}:")
    display_transaction(transaction)
    print("Signature:", transaction.sign_transaction())
    print("*" * 50)

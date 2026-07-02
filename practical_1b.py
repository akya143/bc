import Crypto
import binascii
import datetime
import collections
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA


class Client:
    def __init__(self):
        random_generator = Crypto.Random.new().read
        self._private_key = RSA.generate(1024, random_generator)
        self._public_key = self._private_key.publickey()
        self._signer = PKCS1_v1_5.new(self._private_key)

    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')


class Transaction:
    def __init__(self, sender, receiver, value):
        self.sender = sender
        self.receiver = receiver
        self.value = value
        self.time = datetime.datetime.now()

    def to_dict(self):
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
        if self.sender == "Genesis":
            return "Genesis Transaction - No Signature"
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')


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


# Demo
print("-" * 50)
print("Practical 1b: Creating and Displaying Multiple Transactions")
print("-" * 50)

ninad = Client()
ks = Client()
vighnesh = Client()
sairaj = Client()

print("Ninad's Key:", ninad.identity)
print("KS's Key:", ks.identity)
print("Vighnesh's Key:", vighnesh.identity)
print("Sairaj's Key:", sairaj.identity)
print("-" * 50)

transactions = []

t1 = Transaction(ninad, ks.identity, 15.0)
t1_signature = t1.sign_transaction()
transactions.append(t1)

t2 = Transaction(ninad, vighnesh.identity, 6.0)
t2_signature = t2.sign_transaction()
transactions.append(t2)

t3 = Transaction(ninad, sairaj.identity, 16.0)
t3_signature = t3.sign_transaction()
transactions.append(t3)

t4 = Transaction(vighnesh, ninad.identity, 8.0)
t4_signature = t4.sign_transaction()
transactions.append(t4)

t5 = Transaction(vighnesh, ks.identity, 19.0)
t5_signature = t5.sign_transaction()
transactions.append(t5)

t6 = Transaction(vighnesh, sairaj.identity, 35.0)
t6_signature = t6.sign_transaction()
transactions.append(t6)

t7 = Transaction(sairaj, vighnesh.identity, 5.0)
t7_signature = t7.sign_transaction()
transactions.append(t7)

t8 = Transaction(sairaj, ninad.identity, 12.0)
t8_signature = t8.sign_transaction()
transactions.append(t8)

t9 = Transaction(sairaj, ks.identity, 25.0)
t9_signature = t9.sign_transaction()
transactions.append(t9)

t10 = Transaction(ninad, ks.identity, 1.0)
t10_signature = t10.sign_transaction()
transactions.append(t10)

print("Displaying all created transactions:")
for i, transaction in enumerate(transactions):
    print(f"\nTransaction {i+1}:")
    display_transaction(transaction)
    print("Signature:", transaction.sign_transaction())
    print("*" * 50)

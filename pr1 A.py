import binascii
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA
from Cryptodome import Random


class Client:
    def __init__(self):
        # Random generator
        random_generator = Random.new().read

        # Generate keys
        self._private_key = RSA.generate(1024, random_generator)
        self._public_key = self._private_key.publickey()

        # Signer
        self._signer = PKCS1_v1_5.new(self._private_key)

    @property
    def identity(self):
        return binascii.hexlify(
            self._public_key.export_key(format='DER')
        ).decode('ascii')

    def encrypt_message(self, public_key_hex, message):
        try:
            recipient_key = RSA.import_key(
                binascii.unhexlify(public_key_hex)
            )

            cipher = PKCS1_OAEP.new(recipient_key)
            encrypted = cipher.encrypt(message.encode('utf-8'))

            return encrypted

        except ValueError as e:
            print("Encryption Error:", e)
            return None

    def decrypt_message(self, encrypted_message):
        try:
            cipher = PKCS1_OAEP.new(self._private_key)
            decrypted = cipher.decrypt(encrypted_message)

            return decrypted.decode('utf-8')

        except ValueError as e:
            print("Decryption Error:", e)
            return None

    def sign_message(self, message):
        h = SHA.new(message.encode('utf-8'))
        signature = self._signer.sign(h)

        return binascii.hexlify(signature).decode('ascii')

    def verify_signature(self, public_key_hex, message, signature_hex):
        try:
            sender_key = RSA.import_key(
                binascii.unhexlify(public_key_hex)
            )

            verifier = PKCS1_v1_5.new(sender_key)
            h = SHA.new(message.encode('utf-8'))

            return verifier.verify(
                h,
                binascii.unhexlify(signature_hex)
            )

        except (ValueError, TypeError) as e:
            print("Verification Error:", e)
            return False


# ---------------- DEMO ---------------- #

print("-" * 50)
print("Practical: Secure Messaging Application")
print("-" * 50)

# Create users
alice = Client()
bob = Client()

print("Alice Public Key:", alice.identity)
print("Bob Public Key:", bob.identity)

print("-" * 50)

# Alice sends message
msg = "Hello Bob, this is a secret message from Alice!"
print("Alice Message:", msg)

encrypted = alice.encrypt_message(bob.identity, msg)

if encrypted:
    print("Encrypted:", encrypted)

    decrypted = bob.decrypt_message(encrypted)

    print("Bob Decrypted:", decrypted)
    print("Decryption Successful:", msg == decrypted)

print("-" * 50)

# Bob signs message
msg2 = "Alice, I received your message. Thanks!"
print("Bob Message:", msg2)

signature = bob.sign_message(msg2)
print("Signature:", signature)

print("-" * 50)

# Alice verifies
valid = alice.verify_signature(bob.identity, msg2, signature)
print("Signature Valid:", valid)

# Tampered check
tampered = "Alice, I received your message. Thanks! (changed)"
tampered_valid = alice.verify_signature(bob.identity, tampered, signature)

print("Tampered Signature Valid:", tampered_valid, "(should be False)")

print("-" * 50)

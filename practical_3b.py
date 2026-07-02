import math
import hashlib


class Calculator:
    """
    Demonstrates function overloading and mathematical functions.
    """

    def __init__(self):
        print("Calculator initialized.")

    # --- Function Overloading (Pythonic Way) ---
    def add(self, a, b=None, c=None):
        if c is not None:
            print(f"\n--- Calling add({a}, {b}, {c}) ---")
            result = a + b + c
            print(f"Sum of three numbers: {result}")
            return result
        elif b is not None:
            print(f"\n--- Calling add({a}, {b}) ---")
            result = a + b
            print(f"Sum of two numbers: {result}")
            return result
        else:
            print(f"\n--- Calling add({a}) ---")
            result = a + 10
            print(f"Adding 10 to single number: {result}")
            return result

    # --- Mathematical Functions ---
    def perform_math_operations(self, x, y, k):
        print(f"\n--- Performing Mathematical Operations with x={x}, y={y}, k={k} ---")
        print(f"Addition: {x} + {y} = {x + y}")
        print(f"Subtraction: {x} - {y} = {x - y}")
        print(f"Multiplication: {x} * {y} = {x * y}")
        if y != 0:
            print(f"Division: {x} / {y} = {x / y} (float)")
            print(f"Integer Division: {x} // {y} = {x // y}")
            print(f"Modulo: {x} % {y} = {x % y}")
        else:
            print("Division/Modulo by zero is not allowed.")
        if k != 0:
            add_mod_result = (x + y) % k
            mul_mod_result = (x * y) % k
            print(f"Modular Addition ({x} + {y}) % {k} = {add_mod_result}")
            print(f"Modular Multiplication ({x} * {y}) % {k} = {mul_mod_result}")
        else:
            print("Modular operations require non-zero modulus.")
        print(f"Power: {x} ** {y} = {x ** y}")
        print(f"Square Root of {abs(x)}: {math.sqrt(abs(x))}")
        print("-" * 30)


class CryptographicFunctions:
    """
    Demonstrates common cryptographic hashing functions.
    """

    def __init__(self):
        print("Cryptographic functions utility initialized.")

    def generate_sha256_hash(self, data_string):
        print(f"\n--- Generating SHA-256 Hash for: '{data_string}' ---")
        hashed_data = hashlib.sha256(data_string.encode('utf-8')).hexdigest()
        print(f"SHA-256 Hash: {hashed_data}")
        return hashed_data

    def demonstrate_avalanche_effect(self, base_string):
        print(f"\n--- Demonstrating Avalanche Effect ---")
        print(f"Base string: '{base_string}'")
        hash1 = self.generate_sha256_hash(base_string)
        slightly_changed_string = base_string + "a"
        print(f"Slightly changed string: '{slightly_changed_string}'")
        hash2 = self.generate_sha256_hash(slightly_changed_string)
        print(f"Hash 1: {hash1}")
        print(f"Hash 2: {hash2}")
        print(f"Hashes are different: {hash1 != hash2}")
        print("This illustrates the sensitivity of cryptographic hashes to input changes.")
        print("-" * 30)

    def simple_password_hasher(self, password):
        print(f"\n--- Simple Password Hashing ---")
        salt = hashlib.sha256(b"my_random_salt_for_security").hexdigest().encode('utf-8')
        hashed_password = hashlib.sha256(password.encode('utf-8') + salt).hexdigest()
        print(f"Original Password: {password}")
        print(f"Hashed Password (with salt): {hashed_password}")
        return hashed_password


# --- Demo ---
print("--- Practical 3b: Overloading, Math, and Crypto Functions Demonstration ---")

calc = Calculator()
calc.add(5)
calc.add(5, 10)
calc.add(5, 10, 15)
calc.perform_math_operations(10, 3, 7)
calc.perform_math_operations(15, 0, 5)
calc.perform_math_operations(2, 4, 10)

crypto_util = CryptographicFunctions()
crypto_util.generate_sha256_hash("Hello Blockchain")
crypto_util.generate_sha256_hash("The quick brown fox jumps over the lazy dog")
crypto_util.generate_sha256_hash("The quick brown fox jumps over the lazy cog")
crypto_util.demonstrate_avalanche_effect("secret phrase")
crypto_util.simple_password_hasher("mySecretPass123!")
crypto_util.simple_password_hasher("mySecretPass123!")
crypto_util.simple_password_hasher("anotherPassword")

print("\n--- Demonstration Complete ---")

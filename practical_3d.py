import logging

# --- Conceptual Library 1: Math Utilities ---
class MathUtils:
    @staticmethod
    def square(num):
        return num * num

    @staticmethod
    def safe_divide(numerator, denominator):
        if denominator == 0:
            raise ValueError("Division by zero is not allowed.")
        return numerator / denominator


# --- Conceptual Library 2: String Utilities ---
class StringUtils:
    @staticmethod
    def concatenate_strings(s1, s2):
        return s1 + s2

    @staticmethod
    def reverse_string(s):
        return s[::-1]


# --- Event System using logging ---
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')


class EventLogger:
    @staticmethod
    def emit_deposit_event(user_address, amount, new_balance):
        logging.info(f"EVENT: Deposit - User: {user_address}, Amount: {amount}, New Balance: {new_balance}")

    @staticmethod
    def emit_withdrawal_event(user_address, amount, new_balance):
        logging.info(f"EVENT: Withdrawal - User: {user_address}, Amount: {amount}, New Balance: {new_balance}")

    @staticmethod
    def emit_custom_event(event_name, **kwargs):
        log_message = f"EVENT: {event_name}"
        for key, value in kwargs.items():
            log_message += f", {key}: {value}"
        logging.info(log_message)


# --- Custom Exception ---
class InsufficientFundsError(Exception):
    def __init__(self, sender, requested, available):
        self.message = f"Sender {sender} requested {requested}, but only has {available}."
        super().__init__(self.message)


# --- Main Class for Account Management ---
class AccountManager:
    def __init__(self):
        self.balances = {}
        print("AccountManager initialized.")

    def deposit(self, user_address, amount):
        print(f"\nAttempting deposit for {user_address}: {amount}")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balances[user_address] = self.balances.get(user_address, 0) + amount
        EventLogger.emit_deposit_event(user_address, amount, self.balances[user_address])
        print(f"Deposit successful for {user_address}. New balance: {self.balances[user_address]}")

    def withdraw(self, user_address, amount):
        print(f"\nAttempting withdrawal for {user_address}: {amount}")
        try:
            if amount <= 0:
                raise ValueError("Withdrawal amount must be positive.")
            current_balance = self.balances.get(user_address, 0)
            if current_balance < amount:
                raise InsufficientFundsError(user_address, amount, current_balance)
            self.balances[user_address] -= amount
            EventLogger.emit_withdrawal_event(user_address, amount, self.balances[user_address])
            print(f"Withdrawal successful for {user_address}. New balance: {self.balances[user_address]}")
        except InsufficientFundsError as e:
            logging.error(f"WITHDRAWAL FAILED (Insufficient Funds): {e}")
        except ValueError as e:
            logging.error(f"WITHDRAWAL FAILED (Invalid Amount): {e}")
        except Exception as e:
            logging.error(f"Unexpected error during withdrawal: {e}")

    def get_balance(self, user_address):
        return self.balances.get(user_address, 0)

    def process_data(self, data_list):
        print(f"\nProcessing data list: {data_list}")
        try:
            squared_sum = 0
            for item in data_list:
                squared_sum += MathUtils.square(item)
            logging.info(f"Sum of squares is {squared_sum}")
            assert len(data_list) > 0, "Data list should not be empty!"
            logging.info("Assertion passed: Data list is not empty.")
        except AssertionError as e:
            logging.critical(f"CRITICAL ERROR (Assertion Failed): {e}")
        except Exception as e:
            logging.error(f"Error during data processing: {e}")


# --- Demo ---
print("--- Practical 3d: Libraries, Events, Error Handling Demonstration ---")

acc_mgr = AccountManager()

print("\n--- Library Usage Demo ---")
num = 7
print(f"Square of {num}: {MathUtils.square(num)}")

try:
    result = MathUtils.safe_divide(10, 2)
    print(f"Safe divide 10/2: {result}")
except ValueError as e:
    print(f"Error: {e}")

try:
    result = MathUtils.safe_divide(10, 0)
    print(f"Safe divide 10/0: {result}")
except ValueError as e:
    print(f"Caught error: {e}")

str1 = "Blockchain"
str2 = "Python"
print(f"Concatenation: {StringUtils.concatenate_strings(str1, str2)}")
print(f"Reverse '{str1}': {StringUtils.reverse_string(str1)}")

print("\n--- Events and Error Handling Demo ---")
user_alice = "0xAliceAddress"
user_bob = "0xBobAddress"

try:
    acc_mgr.deposit(user_alice, 100)
except ValueError as e:
    print(f"Caught deposit error: {e}")

try:
    acc_mgr.deposit(user_bob, 50)
except ValueError as e:
    print(f"Caught deposit error: {e}")

try:
    acc_mgr.deposit(user_alice, -10)
except ValueError as e:
    print(f"Caught deposit error: {e}")

acc_mgr.withdraw(user_alice, 30)
acc_mgr.withdraw(user_bob, 70)
acc_mgr.withdraw(user_alice, 0)

print("\n--- Assertion Demo ---")
acc_mgr.process_data([1, 2, 3, 4, 5])
acc_mgr.process_data([])

print("\n--- Demonstration Complete ---")

from abc import ABC, abstractmethod


# --- Conceptual "Contract" (Regular Class) ---
class BaseContract:
    def __init__(self, initial_value):
        self.contract_id = id(self)
        self.data_storage = initial_value
        print(f"BaseContract (ID: {self.contract_id}) initialized with data: {self.data_storage}")

    def get_data(self):
        print(f"BaseContract (ID: {self.contract_id}): Retrieving data: {self.data_storage}")
        return self.data_storage

    def _internal_helper(self, a, b):
        result = a * b
        print(f"BaseContract: Internal helper calculated {a} * {b} = {result}")
        return result

    def get_type(self):
        return "BaseContract"


# --- Inheritance ---
class DerivedContract(BaseContract):
    def __init__(self, initial_value, specific_message):
        super().__init__(initial_value)
        self.derived_message = specific_message
        print(f"DerivedContract (ID: {self.contract_id}) initialized with message: '{self.derived_message}'")

    def get_derived_info(self):
        info = f"Derived message: '{self.derived_message}', Base data: {self.data_storage}"
        print(f"DerivedContract (ID: {self.contract_id}): {info}")
        return info

    def use_base_internal(self, x, y):
        print(f"DerivedContract: Calling base internal helper...")
        return self._internal_helper(x, y)

    def get_type(self):
        return "DerivedContract"


# --- Conceptual "Interface" (Abstract Base Class) ---
class IToken(ABC):
    @abstractmethod
    def get_total_supply(self):
        pass

    @abstractmethod
    def get_balance(self, address):
        pass

    @abstractmethod
    def transfer(self, sender, receiver, amount):
        pass


# --- Conceptual "Abstract Contract" ---
class AbstractERC20Token(IToken):
    def __init__(self, initial_supply, token_name, token_symbol):
        self._total_supply = initial_supply
        self._name = token_name
        self._symbol = token_symbol
        self._balances = {}
        self._balances["deployer_address"] = initial_supply
        print(f"\nAbstractERC20Token initialized: {token_name} ({token_symbol}) with {initial_supply} supply.")

    def get_total_supply(self):
        return self._total_supply

    @abstractmethod
    def get_balance(self, address):
        pass

    def get_token_info(self):
        return f"{self._name} ({self._symbol}), Total Supply: {self._total_supply}"


# --- Concrete Implementation ---
class MyERC20Token(AbstractERC20Token):
    def __init__(self, initial_supply, token_name, token_symbol):
        super().__init__(initial_supply, token_name, token_symbol)
        print(f"MyERC20Token (concrete) fully initialized.")

    def get_balance(self, address):
        return self._balances.get(address, 0)

    def transfer(self, sender, receiver, amount):
        print(f"\n--- Attempting transfer from {sender} to {receiver} for {amount} tokens ---")
        if self._balances.get(sender, 0) >= amount:
            self._balances[sender] -= amount
            self._balances[receiver] = self._balances.get(receiver, 0) + amount
            print(f"Transfer successful! {sender}'s balance: {self.get_balance(sender)}, {receiver}'s balance: {self.get_balance(receiver)}")
            return True
        else:
            print(f"Transfer failed! {sender} has insufficient funds (current: {self.get_balance(sender)}).")
            return False


# --- Demo ---
print("--- Practical 3c: Contracts, Inheritance, Abstract, Interfaces Demo ---")

print("\n--- Base and Derived Contract Demo ---")
base_instance = BaseContract(10)
base_instance.get_data()
print(f"Base instance type: {base_instance.get_type()}")

derived_instance = DerivedContract(50, "Hello World from Derived")
derived_instance.get_data()
derived_instance.get_derived_info()
derived_instance.use_base_internal(3, 7)
print(f"Derived instance type: {derived_instance.get_type()}")

print("\n--- Abstract Contract and Interface Demo ---")
try:
    abstract_token = AbstractERC20Token(1000, "AbstractCoin", "ABC")
except TypeError as e:
    print(f"Error: Cannot instantiate abstract class directly: {e}")

my_token = MyERC20Token(1000, "MyCoin", "MYC")
print(my_token.get_token_info())

addr1 = "0xAlice"
addr2 = "0xBob"
addr3 = "0xCharlie"
deployer_address = "deployer_address"

print(f"\nInitial balance of {deployer_address}: {my_token.get_balance(deployer_address)}")
print(f"Initial balance of {addr1}: {my_token.get_balance(addr1)}")

my_token.transfer(deployer_address, addr1, 200)
my_token.transfer(addr1, addr2, 50)
my_token.transfer(addr2, addr3, 10)
my_token.transfer(addr1, addr2, 500)

print(f"\nFinal balance of {deployer_address}: {my_token.get_balance(deployer_address)}")
print(f"Final balance of {addr1}: {my_token.get_balance(addr1)}")
print(f"Final balance of {addr2}: {my_token.get_balance(addr2)}")
print(f"Final balance of {addr3}: {my_token.get_balance(addr3)}")

print("\n--- Demonstration Complete ---")

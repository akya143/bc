import datetime


class SmartContractSimulation:
    """
    A Python class to conceptually simulate a Solidity smart contract's function types.
    """

    def __init__(self, initial_data=100):
        self.stored_data = initial_data
        print(f"Contract initialized with stored_data: {self.stored_data}")

    # --- Regular Function (Modifies State) ---
    def set_data(self, new_value):
        print(f"\n--- Calling regular function: set_data({new_value}) ---")
        old_value = self.stored_data
        self.stored_data = new_value
        print(f"Stored data updated from {old_value} to {self.stored_data}")

    # --- View Function (Reads State, No Modification) ---
    def get_data(self):
        print(f"\n--- Calling view function: get_data() ---")
        print(f"Current stored data: {self.stored_data}")
        return self.stored_data

    def get_status(self):
        print(f"\n--- Calling view function: get_status() ---")
        status = f"Data: {self.stored_data}, Last Checked: {datetime.datetime.now()}"
        print(f"Status report: {status}")
        return status

    # --- Pure Function (No State Interaction) ---
    @staticmethod
    def calculate_sum(a, b):
        print(f"\n--- Calling pure function: calculate_sum({a}, {b}) ---")
        result = a + b
        print(f"Result: {result}")
        return result

    # --- Fallback Function (Conceptual) ---
    def __getattr__(self, name):
        print(f"\n--- Fallback triggered for method: {name} ---")

        def method_not_found(*args, **kwargs):
            print(f"Warning: Method '{name}' does not exist in this contract simulation.")
            print(f"Arguments passed: {args}, Keyword arguments: {kwargs}")
            print("This conceptually represents an unhandled transaction/call on a blockchain.")
            return None

        return method_not_found

    def __call__(self, *args, **kwargs):
        print(f"\n--- Instance called directly (conceptual receive/fallback) ---")
        print(f"Simulating direct interaction or plain value transfer.")
        print(f"Arguments: {args}, Kwargs: {kwargs}")


# --- Demo ---
print("--- Practical 3a: Function Types Demonstration ---")

my_contract = SmartContractSimulation()

# 1. Regular Function
my_contract.set_data(250)
my_contract.set_data(75)

# 2. View Functions
current_data = my_contract.get_data()
status_report = my_contract.get_status()

# 3. Pure Function
pure_result = SmartContractSimulation.calculate_sum(10, 20)
another_pure_result = SmartContractSimulation.calculate_sum(current_data, 50)

# 4. Fallback Function
my_contract.non_existent_method("hello", 123, option="test")
my_contract("direct_call_data", amount=10)

print("\n--- Demonstration Complete ---")
print(f"Final stored_data value: {my_contract.stored_data}")

class SimpleNFTCollection:
    """
    A Python class that simulates the core logic of an ERC-721 NFT collection.
    """

    def __init__(self, name, symbol):
        self._name = name
        self._symbol = symbol
        self._next_token_id = 0
        self._owners = {}
        self._balances = {}
        self._token_approvals = {}
        self._operator_approvals = {}
        self._token_uris = {}
        print(f"NFT Collection '{self._name}' ({self._symbol}) initialized.")

    def name(self):
        return self._name

    def symbol(self):
        return self._symbol

    def _require(self, condition, error_message):
        if not condition:
            raise ValueError(error_message)

    def balance_of(self, owner_address):
        self._require(owner_address != "0x0000000000000000000000000000000000000000",
                      "ERC721: address zero is not a valid owner")
        return self._balances.get(owner_address, 0)

    def owner_of(self, token_id):
        owner = self._owners.get(token_id)
        self._require(owner is not None, f"ERC721: owner query for nonexistent token ID {token_id}")
        return owner

    def mint(self, to_address, token_uri):
        self._require(to_address != "0x0000000000000000000000000000000000000000",
                      "ERC721: mint to the zero address")
        token_id = self._next_token_id
        self._next_token_id += 1
        self._owners[token_id] = to_address
        self._balances[to_address] = self._balances.get(to_address, 0) + 1
        self._token_uris[token_id] = token_uri
        print(f"\nMINTED: Token ID {token_id} assigned to {to_address}. URI: {token_uri}")
        return token_id

    def _is_approved_or_owner(self, spender, token_id):
        owner = self.owner_of(token_id)
        if spender == owner:
            return True
        if self._token_approvals.get(token_id) == spender:
            return True
        if self._operator_approvals.get(owner, {}).get(spender, False):
            return True
        return False

    def transfer_from(self, from_address, to_address, token_id, caller_address):
        print(f"\nTRANSFER: Attempting to transfer Token ID {token_id} from {from_address} to {to_address}")
        self._require(self.owner_of(token_id) == from_address,
                      f"ERC721: transfer from incorrect owner. Token {token_id} owned by {self.owner_of(token_id)}")
        self._require(to_address != "0x0000000000000000000000000000000000000000",
                      "ERC721: transfer to the zero address")
        self._require(self._is_approved_or_owner(caller_address, token_id),
                      f"ERC721: caller {caller_address} is not owner nor approved for Token ID {token_id}")
        self._balances[from_address] -= 1
        self._owners[token_id] = to_address
        self._balances[to_address] = self._balances.get(to_address, 0) + 1
        if token_id in self._token_approvals:
            del self._token_approvals[token_id]
        print(f"SUCCESS: Token ID {token_id} transferred from {from_address} to {to_address}")

    def approve(self, approved_address, token_id, caller_address):
        print(f"\nAPPROVE: {caller_address} approves {approved_address} for Token ID {token_id}")
        owner = self.owner_of(token_id)
        self._require(approved_address != owner, "ERC721: approval to current owner")
        self._require(caller_address == owner or self.is_approved_for_all(owner, caller_address),
                      "ERC721: approve caller is not owner nor approved for all")
        self._token_approvals[token_id] = approved_address
        print(f"SUCCESS: {approved_address} is now approved for Token ID {token_id}")

    def get_approved(self, token_id):
        self._require(token_id in self._owners,
                      f"ERC721: approved query for nonexistent token ID {token_id}")
        return self._token_approvals.get(token_id, "0x0000000000000000000000000000000000000000")

    def set_approval_for_all(self, operator_address, approved_status, caller_address):
        print(f"\nSET APPROVAL FOR ALL: {caller_address} sets {operator_address} as operator: {approved_status}")
        self._require(caller_address != operator_address, "ERC721: approve to caller")
        if caller_address not in self._operator_approvals:
            self._operator_approvals[caller_address] = {}
        self._operator_approvals[caller_address][operator_address] = approved_status
        print(f"SUCCESS: {operator_address} is now {'approved' if approved_status else 'disapproved'} as operator for {caller_address}")

    def is_approved_for_all(self, owner_address, operator_address):
        return self._operator_approvals.get(owner_address, {}).get(operator_address, False)

    def token_uri(self, token_id):
        self._require(token_id in self._owners,
                      f"ERC721: URI query for nonexistent token ID {token_id}")
        return self._token_uris.get(token_id)


# --- Demo ---
print("--- Practical 4a: NFT Interaction (Python Simulation) Demonstration ---")

my_nft_collection = SimpleNFTCollection("MyAwesomeNFTs", "MANFT")

alice_address = "0xAliceWallet"
bob_address = "0xBobWallet"
charlie_address = "0xCharlieWallet"
marketplace_address = "0xMarketplaceContract"

# Mint NFTs
print("\n--- Minting NFTs ---")
token_id_0 = my_nft_collection.mint(alice_address, "https://my-nft-data.com/0")
token_id_1 = my_nft_collection.mint(bob_address, "https://my-nft-data.com/1")
token_id_2 = my_nft_collection.mint(alice_address, "https://my-nft-data.com/2")

# Query NFT Ownership and Metadata
print("\n--- Querying NFTs ---")
print(f"Alice's balance: {my_nft_collection.balance_of(alice_address)}")
print(f"Bob's balance: {my_nft_collection.balance_of(bob_address)}")
print(f"Owner of Token ID {token_id_0}: {my_nft_collection.owner_of(token_id_0)}")
print(f"URI of Token ID {token_id_1}: {my_nft_collection.token_uri(token_id_1)}")

try:
    my_nft_collection.owner_of(999)
except ValueError as e:
    print(f"Error querying non-existent token: {e}")

# Transfer NFTs
print("\n--- Transferring NFTs ---")
try:
    my_nft_collection.transfer_from(alice_address, charlie_address, token_id_0, alice_address)
    print(f"Alice's balance after transfer: {my_nft_collection.balance_of(alice_address)}")
    print(f"Charlie's balance after transfer: {my_nft_collection.balance_of(charlie_address)}")
    print(f"New owner of Token ID {token_id_0}: {my_nft_collection.owner_of(token_id_0)}")
except ValueError as e:
    print(f"Transfer failed: {e}")

try:
    my_nft_collection.transfer_from(alice_address, bob_address, token_id_2, bob_address)
except ValueError as e:
    print(f"Invalid transfer attempt failed: {e}")

# Approve and Transfer
print("\n--- Delegated Transfer (Approve and TransferFrom) ---")
my_nft_collection.approve(marketplace_address, token_id_2, alice_address)
print(f"Approved address for Token ID {token_id_2}: {my_nft_collection.get_approved(token_id_2)}")

try:
    my_nft_collection.transfer_from(alice_address, bob_address, token_id_2, marketplace_address)
    print(f"Alice's balance after delegated transfer: {my_nft_collection.balance_of(alice_address)}")
    print(f"Bob's balance after delegated transfer: {my_nft_collection.balance_of(bob_address)}")
    print(f"New owner of Token ID {token_id_2}: {my_nft_collection.owner_of(token_id_2)}")
except ValueError as e:
    print(f"Delegated transfer failed: {e}")

# Set Approval for All (Operator)
print("\n--- Set Approval For All (Operator) ---")
my_nft_collection.set_approval_for_all(marketplace_address, True, charlie_address)
print(f"Is Marketplace approved for all of Charlie's tokens? {my_nft_collection.is_approved_for_all(charlie_address, marketplace_address)}")

try:
    my_nft_collection.transfer_from(charlie_address, alice_address, token_id_0, marketplace_address)
    print(f"Charlie's balance after operator transfer: {my_nft_collection.balance_of(charlie_address)}")
    print(f"Alice's balance after operator transfer: {my_nft_collection.balance_of(alice_address)}")
    print(f"New owner of Token ID {token_id_0}: {my_nft_collection.owner_of(token_id_0)}")
except ValueError as e:
    print(f"Operator transfer failed: {e}")

print("\n--- NFT Interaction Demonstration Complete ---")

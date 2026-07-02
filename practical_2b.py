import requests
import json
import datetime


def get_current_block_info():
    print("\n--- Fetching Current Block Information ---")
    try:
        response = requests.get("https://blockchain.info/latestblock")
        response.raise_for_status()
        block_info = response.json()
        print("Current Block Information:")
        print(f"Block Height: {block_info.get('height', 'N/A')}")
        print(f"Block Hash: {block_info.get('hash', 'N/A')}")
        print(f"Block Index: {block_info.get('block_index', 'N/A')}")
        print(f"Timestamp: {block_info.get('time', 'N/A')} (Unix Timestamp)")
        print(f"Version: {block_info.get('version', 'N/A')}")
        print(f"Previous Block Hash: {block_info.get('prev_block_hash', 'N/A')}")
        print(f"Merkle Root: {block_info.get('mrkl_root', 'N/A')}")
        print(f"Nonce: {block_info.get('nonce', 'N/A')}")
        print(f"Bits: {block_info.get('bits', 'N/A')}")
        print(f"Transaction Count: {block_info.get('n_tx', 'N/A')}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching current block info: {e}")
    except json.JSONDecodeError:
        print("Error: Could not decode JSON response for latest block.")
    print("-" * 50)


def get_address_balance(address):
    print(f"\n--- Fetching Balance for Address: {address} ---")
    try:
        response = requests.get(f"https://blockchain.info/q/addressbalance/{address}")
        response.raise_for_status()
        balance_satoshi = int(response.text)
        balance_btc = balance_satoshi / 10**8
        print(f"Balance of address {address}: {balance_btc:.8f} BTC ({balance_satoshi} Satoshis)")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching address balance: {e}")
    except ValueError:
        print(f"Error: Could not parse balance for address {address}.")
    print("-" * 50)


def get_address_transactions(address):
    print(f"\n--- Fetching Recent Transactions for Address: {address} ---")
    try:
        response = requests.get(f"https://blockchain.info/rawaddr/{address}")
        response.raise_for_status()
        address_info = response.json()
        transactions = address_info.get('txs', [])
        if not transactions:
            print(f"No transactions found for address {address} in recent history.")
            return
        print(f"Recent Transactions for {address}:")
        for i, tx in enumerate(transactions[:5]):
            print(f"\n  Transaction {i+1}:")
            print(f"  TX ID: {tx.get('hash', 'N/A')}")
            print(f"  Time: {datetime.datetime.fromtimestamp(tx.get('time', 0))}")
            print(f"  Fee: {tx.get('fee', 0) / 10**8:.8f} BTC")
            total_sent = 0
            total_received = 0
            for vin in tx.get('inputs', []):
                prev_out = vin.get('prev_out', {})
                if prev_out.get('addr') == address:
                    total_sent += prev_out.get('value', 0)
            for vout in tx.get('out', []):
                if vout.get('addr') == address:
                    total_received += vout.get('value', 0)
            if total_sent > 0:
                print(f"  Amount Sent by {address}: {total_sent / 10**8:.8f} BTC")
            if total_received > 0:
                print(f"  Amount Received by {address}: {total_received / 10**8:.8f} BTC")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching address transactions: {e}")
    except json.JSONDecodeError:
        print("Error: Could not decode JSON response for address transactions.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    print("-" * 50)


if __name__ == "__main__":
    print("-" * 50)
    print("Practical 2b: Bitcoin API Demonstration")
    print("-" * 50)

    get_current_block_info()

    sample_address = "3Dh2ft6UsqjbTNzs5zrp7uK17Gqg1Pg5u5"
    get_address_balance(sample_address)
    get_address_transactions(sample_address)

    print("\nBitcoin API Demonstration Complete.")
    print("Note: For direct Bitcoin Core node interaction, you would use RPC commands (e.g., bitcoin-cli)")
    print("or an RPC client library in Python (e.g., python-bitcoinrpc) to a locally running 'bitcoind'.")
    print("-" * 50)

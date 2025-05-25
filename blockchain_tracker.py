from web3 import Web3
import pandas as pd
import time

# Step 1: Connect to local Ganache blockchain
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Step 2: Verify connection
if web3.is_connected():
    print("Connected to Ganache successfully!")
else:
    raise Exception("Connection failed. Ensure Ganache is running.")

# Step 3: Set the deployed smart contract address
contract_address = "0x777F244285f37397E7801dfDDE64DF8F96B75F3b"  # ✅ Your deployed contract address

# Step 4: Load the ABI from your IoTDataStorage contract
abi = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"},
            {"indexed": False, "internalType": "string", "name": "packageId", "type": "string"},
            {"indexed": False, "internalType": "string", "name": "dataType", "type": "string"},
            {"indexed": False, "internalType": "string", "name": "dataValue", "type": "string"}
        ],
        "name": "DataStored",
        "type": "event"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "index", "type": "uint256"}],
        "name": "getRecord",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {"internalType": "string", "name": "", "type": "string"},
            {"internalType": "string", "name": "", "type": "string"},
            {"internalType": "string", "name": "", "type": "string"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getTotalRecords",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "_packageId", "type": "string"},
            {"internalType": "string", "name": "_dataType", "type": "string"},
            {"internalType": "string", "name": "_dataValue", "type": "string"}
        ],
        "name": "storeData",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Step 5: Load the contract and set default account
contract = web3.eth.contract(address=contract_address, abi=abi)
web3.eth.default_account = web3.eth.accounts[0]
print(f"Smart Contract loaded at: {contract_address}")

# Step 6: Store a dummy logistics reading
txn = contract.functions.storeData("TEST001", "Temperature", "22.5°C").transact({
    'from': web3.eth.default_account,
    'gas': 1000000
})
web3.eth.wait_for_transaction_receipt(txn)
print("Dummy logistics data stored on blockchain.")

# Step 7: Check the total records
total = contract.functions.getTotalRecords().call()
print(f"📦 Total logistics records so far: {total}")

if total > 0:
    record = contract.functions.getRecord(0).call()
    print("First Logistics Record:", record)

# Step 8: Load logistics CSV data
df = pd.read_csv("logistics_data.csv")  
print("\nCSV Preview:")
print(df.head())

# Step 9: Define a function to send logistics data to blockchain
def send_iot_data(package_id, data_type, data_value):
    txn = contract.functions.storeData(package_id, data_type, data_value).transact({
        'from': web3.eth.default_account,
        'gas': 3000000
    })
    receipt = web3.eth.wait_for_transaction_receipt(txn)
    print(f"Stored: {package_id} | {data_type} = {data_value} | Txn Hash: {receipt.transactionHash.hex()}")

# Step 10: Loop and send each row from CSV
print("\n Sending logistics IoT data to blockchain...\n")
for _, row in df.iterrows():
    send_iot_data(str(row["device_id"]), str(row["data_type"]), str(row["data_value"]))
    time.sleep(1)  # Prevent flooding the network

# Step 11: Final record confirmation
final_total = contract.functions.getTotalRecords().call()
print(f"\n✅ Final logistics record count: {final_total}")

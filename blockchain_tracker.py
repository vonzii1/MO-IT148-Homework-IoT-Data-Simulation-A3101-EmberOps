from web3 import Web3
import pandas as pd
import time

# Step 1: Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

if web3.is_connected():
    print("✅ Connected to Ganache successfully!")
else:
    raise Exception("❌ Connection failed. Start Ganache GUI first.")

# Step 2: Replace this with your actual deployed contract address
contract_address = "0x777F244285f37397E7801dfDDE64DF8F96B75F3b"

# Step 3: ABI from IoTDataStorage_metadata.json
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

# Step 4: Load the contract and set sender
contract = web3.eth.contract(address=contract_address, abi=abi)
web3.eth.default_account = web3.eth.accounts[0]
print(f"✅ Smart Contract loaded at: {contract_address}")

# Step 5: Send dummy test data
txn = contract.functions.storeData("TEST001", "Temperature", "22.5°C").transact({
    'from': web3.eth.default_account,
    'gas': 1000000
})
web3.eth.wait_for_transaction_receipt(txn)
print("✅ Dummy data stored on blockchain.")

# Step 6: Confirm it's stored
total = contract.functions.getTotalRecords().call()
print(f"📊 Total records so far: {total}")

if total > 0:
    record = contract.functions.getRecord(0).call()
    print("🔍 First Record:", record)

# Step 7: Load CSV and preview
df = pd.read_csv("formatted_healthcare_data.csv")  # <== Make sure this file is in the same folder
print("\n📄 Preview CSV:")
print(df.head())

# Step 8: Define send function
def send_iot_data(package_id, data_type, data_value):
    txn = contract.functions.storeData(package_id, data_type, data_value).transact({
        'from': web3.eth.default_account,
        'gas': 3000000
    })
    receipt = web3.eth.wait_for_transaction_receipt(txn)
    print(f"✅ Stored: {package_id} | {data_type} = {data_value} | Txn Hash: {receipt.transactionHash.hex()}")

# Step 9: Loop and send CSV data
print("\n🚀 Sending all IoT data from CSV...\n")
for _, row in df.iterrows():
    send_iot_data(str(row["device_id"]), str(row["data_type"]), str(row["data_value"]))
    time.sleep(1)  # Delay to avoid overloading

# Step 10: Final check
final_total = contract.functions.getTotalRecords().call()
print(f"✅ Final record count: {final_total}")

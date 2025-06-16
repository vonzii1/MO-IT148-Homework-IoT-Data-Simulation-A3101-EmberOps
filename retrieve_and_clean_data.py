from web3 import Web3
import pandas as pd
import numpy as np

# 1. Connect to Ganache
ganache_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

if not web3.is_connected():
    raise Exception("⚠️ Connection to Ganache failed. Please make sure Ganache is running.")

print("✅ Connected to Ganache!")

# 2. Load contract ABI and address
contract_address = web3.to_checksum_address("0x782b0ED6Bc0AFAA85355e8f6109779e2d5677C90")

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
        "inputs": [
            {"internalType": "string", "name": "_packageId", "type": "string"},
            {"internalType": "string", "name": "_dataType", "type": "string"},
            {"internalType": "string", "name": "_dataValue", "type": "string"}
        ],
        "name": "storeData",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "dataRecords",
        "outputs": [
            {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
            {"internalType": "string", "name": "packageId", "type": "string"},
            {"internalType": "string", "name": "dataType", "type": "string"},
            {"internalType": "string", "name": "dataValue", "type": "string"}
        ],
        "stateMutability": "view",
        "type": "function"
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
    }
]

# 3. Load smart contract
contract = web3.eth.contract(address=contract_address, abi=abi)
print(f"✅ Smart contract loaded at: {contract_address}")

# 4. Retrieve total records
total_records = contract.functions.getTotalRecords().call()
print(f"📦 Total IoT records stored: {total_records}")

# 5. Fetch all records
data = []
for i in range(total_records):
    record = contract.functions.getRecord(i).call()
    data.append({
        "timestamp": record[0],
        "device_id": record[1],
        "data_type": record[2],
        "data_value": record[3]
    })

# 6. Create DataFrame
df = pd.DataFrame(data)

# 7. Convert UNIX timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

# 8. Extract numeric value from 'data_value'
df["numeric_value"] = df["data_value"].str.extract(r'(\d+\.?\d*)').astype(float)

# 9. Fill missing values
df.fillna(0, inplace=True)

# 10. Preview cleaned data
print("\n📊 Cleaned Data Preview:")
print(df.head())

# 11. Save to CSV
df.to_csv("cleaned_iot_data.csv", index=False)
print("\n✅ Cleaned IoT data saved successfully as cleaned_iot_data.csv")

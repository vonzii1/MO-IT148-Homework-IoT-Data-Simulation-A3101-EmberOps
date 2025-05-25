import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

num_records = 100
start_lat = 14.5995  # Sample: Manila
start_long = 120.9842

data = []

for _ in range(num_records):
    record = {
        "timestamp": datetime.now() - timedelta(minutes=np.random.randint(0, 1440)),
        "package_id": f"PKG{np.random.randint(1000, 9999)}",
        "gps_lat": round(start_lat + np.random.uniform(-0.02, 0.02), 6),
        "gps_long": round(start_long + np.random.uniform(-0.02, 0.02), 6),
        "rfid_code": f"RFID-{random.randint(100000, 999999)}",
        "temperature_c": round(np.random.uniform(2.0, 8.0), 1)  # For cold storage goods
    }
    data.append(record)

df = pd.DataFrame(data)

# Save to CSV and JSON
df.to_csv("logistics_data.csv", index=False)
df.to_json("logistics_data.json", orient="records")

print("✅ Logistics data generated and saved.")

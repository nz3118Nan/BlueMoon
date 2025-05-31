import json
import csv
from pathlib import Path

# Read the JSON file
json_path = Path(__file__).parent / 'tmp_sui_data.json'
with open(json_path, 'r') as f:
    data = json.load(f)

# Define the CSV headers
headers = [
    'id',
    'packageId',
    'parentPoolId',
    'poolId',
    'investorId',
    'assetTypes',
    'apr'
]

# Prepare the data for CSV
csv_data = []
for item in data['data']:
    row = {
        'id': item['id'],
        'packageId': item['packageId'],
        'parentPoolId': item['parentPoolId'],
        'poolId': item['poolId'],
        'investorId': item['investorId'],
        'assetTypes': '|'.join(item['assetTypes']),  # Join multiple asset types with pipe
        'apr': item['apr']
    }
    csv_data.append(row)

# Write to CSV
csv_path = Path(__file__).parent / 'vaults_data_sui.csv'
with open(csv_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(csv_data)

print(f"CSV file has been created at: {csv_path}") 
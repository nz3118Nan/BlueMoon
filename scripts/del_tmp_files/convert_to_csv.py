import json
import csv
from pathlib import Path

# Read the JSON file
json_path = Path(__file__).parent / 'tmp_sui_data.json'
with open(json_path, 'r') as f:
    data = json.load(f)

# Define the CSV headers and corresponding JSON paths
headers = [
    'name',
    'address',
    'network',
    'protocol',
    'token_name',
    'token_symbol',
    'token_address',
    'tvl_usd',
    'locked_usd',
    'liquid_usd',
    'number_of_holders',
    'apy_1day',
    'apy_7day',
    'apy_30day',
    'vault_score',
    'vault_tvl_score',
    'protocol_tvl_score',
    'holder_score',
    'network_score',
    'asset_score'
]

# Prepare the data for CSV
csv_data = []
for item in data:
    row = {
        'name': item['name'],
        'address': item['address'],
        'network': item['network'],
        'protocol': item['protocol'],
        'token_name': item['token']['name'],
        'token_symbol': item['token']['symbol'],
        'token_address': item['token']['assetAddress'],
        'tvl_usd': item['tvlDetails']['tvlUsd'],
        'locked_usd': item['tvlDetails']['lockedUsd'],
        'liquid_usd': item['tvlDetails']['liquidUsd'],
        'number_of_holders': item['numberOfHolders'],
        'apy_1day': item['apy']['total']['1day'],
        'apy_7day': item['apy']['total']['7day'],
        'apy_30day': item['apy']['total']['30day'],
        'vault_score': item['score']['vaultScore'],
        'vault_tvl_score': item['score']['vaultTvlScore'],
        'protocol_tvl_score': item['score']['protocolTvlScore'],
        'holder_score': item['score']['holderScore'],
        'network_score': item['score']['networkScore'],
        'asset_score': item['score']['assetScore']
    }
    csv_data.append(row)

# Write to CSV
csv_path = Path(__file__).parent / 'vaults_data.csv'
with open(csv_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(csv_data)

print(f"CSV file has been created at: {csv_path}") 
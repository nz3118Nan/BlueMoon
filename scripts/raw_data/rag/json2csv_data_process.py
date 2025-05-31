#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: rag_init.py
Author: Zhou Nan
Date: 2025-03-18
Description: Initialize the RAG system for the initial check and setup if needed
"""
################################################################################
# system settings
import os
import sys
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
os.chdir(root_dir)
sys.path.append(root_dir)

# built-in modules
import json
from pydantic import BaseModel
import pandas as pd

# developed modules
from app.core.logging_setting import logger
from app.core.config import Config
from app.core.database import db_connection_pool
################################################################################
store_dir = os.path.join(root_dir, 'app/rag_system/preliminary_system_data/kb_1/')
################################################################################
# main function
def base_token_data_process():
    target_kb_id = 1
    # scripts/raw_data/rag/base.tokens.json
    file_path = os.path.join(root_dir, 'scripts/raw_data/rag/base.tokens.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    data = data['data']
    # -----------------------------------------------------------------------# 
    class Network(BaseModel):
        name: str
        chainId: int
    class TokenData(BaseModel):
        address: str
        name: str
        symbol: str
        decimals: int
        network: Network
        
    data = [TokenData(**item) for item in data]
    # -----------------------------------------------------------------------# 
    ## parse data 
    columns = ['key', 'value', 'tags', 'kb_id', 'user_id', 'meta_data']
    data = [
        {
            'key': f"{item.name} ({item.symbol})",
            'value': f"Token Name: {item.name} - Token Asset Address: {item.address} - Token Symbol: {item.symbol} - Token Decimals: {item.decimals} - Network: {item.network.name} - Chain ID: {item.network.chainId}",
            'tags': json.dumps(["token", "base"])   ,
            'kb_id': target_kb_id,
            'user_id': '0',
            'meta_data': {}
        } for item in data
    ]
    # create a data_pd dataframe
    data_pd = pd.DataFrame(data)
    # -----------------------------------------------------------------------# 
    # store data to csv file
    file_name = f'base_tokens_(kb_{target_kb_id}).csv'
    file_path = os.path.join(store_dir, file_name)
    with open(file_path, 'w') as f:
        # store {} empty json object
        f.write(data_pd.to_csv(index=False)) 
    pass

def arbitrum_token_data_process():
    target_kb_id = 1
    # scripts/raw_data/rag/arbitrum.tokens.json
    file_path = os.path.join(root_dir, 'scripts/raw_data/rag/arbitrum.tokens.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    data = data['data']
    # -----------------------------------------------------------------------# 
    ## parse data 
    columns = ['key', 'value', 'tags', 'kb_id', 'user_id', 'meta_data']
    data = [
        {
            'key': f"{item['name']} ({item['symbol']})",
            'value': f"Token Name: {item['name']} - Token Asset Address: {item['address']} - Token Symbol: {item['symbol']} - Token Decimals: {item['decimals']} - Network: {item['network']['name']} - Chain ID: {item['network']['chainId']}",
            'tags': json.dumps(["token", "arbitrum"]),
            'kb_id': target_kb_id,
            'user_id': '0',
            'meta_data': {}
        } for item in data
    ]
    # create a data_pd dataframe
    data_pd = pd.DataFrame(data)
    # -----------------------------------------------------------------------# 
    # store data to csv file
    file_name = f'arbitrum_tokens_(kb_{target_kb_id}).csv'
    file_path = os.path.join(store_dir, file_name)
    with open(file_path, 'w') as f:
        # store {} empty json object
        f.write(data_pd.to_csv(index=False))
    pass

def mainnet_token_data_process():
    target_kb_id = 1
    # scripts/raw_data/rag/mainnet.tokens.json
    file_path = os.path.join(root_dir, 'scripts/raw_data/rag/mainnet.tokens.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    data = data['data']
    # -----------------------------------------------------------------------# 
    ## parse data 
    columns = ['key', 'value', 'tags', 'kb_id', 'user_id', 'meta_data']
    data = [
        {
            'key': f"{item['name']} ({item['symbol']})",
            'value': f"Token Name: {item['name']} - Token Asset Address: {item['address']} - Token Symbol: {item['symbol']} - Token Decimals: {item['decimals']} - Network: {item['network']['name']} - Chain ID: {item['network']['chainId']}",
            'tags': json.dumps(["token", "mainnet"]),
            'kb_id': target_kb_id,
            'user_id': '0',
            'meta_data': {}
        } for item in data
    ]
    # create a data_pd dataframe
    data_pd = pd.DataFrame(data)
    # -----------------------------------------------------------------------# 
    # store data to csv file
    file_name = f'mainnet_tokens_(kb_{target_kb_id}).csv'
    file_path = os.path.join(store_dir, file_name)
    with open(file_path, 'w') as f:
        # store {} empty json object
        f.write(data_pd.to_csv(index=False))
    pass

def optimism_token_data_process():
    target_kb_id = 1
    # scripts/raw_data/rag/optimism.tokens.json
    file_path = os.path.join(root_dir, 'scripts/raw_data/rag/optimism.tokens.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    data = data['data']
    # -----------------------------------------------------------------------# 
    columns = ['key', 'value', 'tags', 'kb_id', 'user_id', 'meta_data'] 
    data = [
        {
            'key': f"{item['name']} ({item['symbol']})",
            'value': f"Token Name: {item['name']} - Token Asset Address: {item['address']} - Token Symbol: {item['symbol']} - Token Decimals: {item['decimals']} - Network: {item['network']['name']} - Chain ID: {item['network']['chainId']}",
            'tags': json.dumps(["token", "optimism"]),
            'kb_id': target_kb_id,
            'user_id': '0',
            'meta_data': {}
        } for item in data
    ]
    # create a data_pd dataframe
    data_pd = pd.DataFrame(data)
    # -----------------------------------------------------------------------# 
    # store data to csv file
    file_name = f'optimism_tokens_(kb_{target_kb_id}).csv'
    file_path = os.path.join(store_dir, file_name)
    with open(file_path, 'w') as f:
        # store {} empty json object
        f.write(data_pd.to_csv(index=False))
    pass

def polygon_token_data_process():
    target_kb_id = 1
    # scripts/raw_data/rag/polygon.tokens.json
    file_path = os.path.join(root_dir, 'scripts/raw_data/rag/polygon.tokens.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    data = data['data']
    # -----------------------------------------------------------------------# 
    ## parse data 
    columns = ['key', 'value', 'tags', 'kb_id', 'user_id', 'meta_data']
    data = [
        {
            'key': f"{item['name']} ({item['symbol']})",
            'value': f"Token Name: {item['name']} - Token Asset Address: {item['address']} - Token Symbol: {item['symbol']} - Token Decimals: {item['decimals']} - Network: {item['network']['name']} - Chain ID: {item['network']['chainId']}",
            'tags': json.dumps(["token", "polygon"]),
            'kb_id': target_kb_id,
            'user_id': '0',
            'meta_data': {}
        } for item in data
    ]
    # create a data_pd dataframe
    data_pd = pd.DataFrame(data)
    # -----------------------------------------------------------------------# 
    # store data to csv file
    file_name = f'polygon_tokens_(kb_{target_kb_id}).csv'
    file_path = os.path.join(store_dir, file_name)
    with open(file_path, 'w') as f:
        # store {} empty json object
        f.write(data_pd.to_csv(index=False))
    pass

def main():
    base_token_data_process()
    arbitrum_token_data_process()
    mainnet_token_data_process()
    optimism_token_data_process()
    polygon_token_data_process()

################################################################################
if __name__ == "__main__":
    main()



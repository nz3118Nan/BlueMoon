# curl -X GET 'https://api.dify.ai/v1/messages?user=abc-123&conversation_id='\
#  --header 'Authorization: Bearer {api_key}'

import requests
from typing import Dict, Any, Optional, List, Union
from requests.exceptions import RequestException
from pydantic import BaseModel, Field
import aiohttp
import asyncio
from abc import ABC, abstractmethod

class Token(BaseModel):
    name: str
    symbol: str
    address: str
    decimals: int

class APYMetrics(BaseModel):
    day1: float = Field(alias="1day", default=0)
    day7: float = Field(alias="7day", default=0)
    day30: float = Field(alias="30day", default=0)

class APY(BaseModel):
    base: APYMetrics
    total: APYMetrics

class Scores(BaseModel):
    provider: str
    assetScore: float
    vaultScore: float
    holderScore: float
    networkScore: float
    vaultTvlScore: float
    protocolTvlScore: float

class Vault_EVM(BaseModel):
    address: str
    chainId: int
    name: str
    description: str
    protocol: str
    numberOfHolders: str
    tvlUsd: str
    tvlNative: str
    token: Token
    apy: APY
    scores: Scores
    hasWithdrawDelay: bool
    network: str
    tags: List[str]

class VaultResponse(BaseModel):
    data: List[Vault_EVM]

class VaultSourcingSystem:
    """
    VaultSourcingSystem aggregates vault data from different networks and APIs.
    Supports EVM, Sui, and Solana networks with async data fetching capabilities.
    """
    
    def __init__(self, conversation_id: str, user_id: str, weight_yield: float = 1.0, weight_risk: float = 1.0):
        """
        Initialize the VaultSourcingSystem.
        
        Args:
            conversation_id (str): Unique identifier for the conversation
            user_id (str): Unique identifier for the user
            weight_yield (float): Weight for yield scoring
            weight_risk (float): Weight for risk scoring
        """
        self.conversation_id = conversation_id
        self.user_id = user_id
        self.weight_yield = weight_yield
        self.weight_risk = weight_risk
        
        # Network fetcher mapping
        self._network_fetchers = {
            "EVM": self._fetch_from_evm,
            "Sui": self._fetch_from_sui,
            "Solana": self._fetch_from_solana
        }
    
    async def fetch_vaults(self, networks: Union[str, List[str]] = "ALL") -> List[Vault_EVM]:
        """
        Fetch vault data from specified networks.
        
        Args:
            networks: Network(s) to fetch from. Can be "ALL", a single network name, or a list of networks
            
        Returns:
            List of sorted vault data
        """
        if networks == "ALL":
            selected_networks = list(self._network_fetchers.keys())
        elif isinstance(networks, str):
            selected_networks = [networks]
        else:
            selected_networks = networks
            
        all_vaults = []
        for network in selected_networks:
            if network in self._network_fetchers:
                fetcher = self._network_fetchers[network]
                try:
                    network_vaults = await fetcher()
                    all_vaults.extend(network_vaults)
                except Exception as e:
                    print(f"Error fetching from {network}: {str(e)}")
                    continue
        
        # Sort vaults by vault score
        return sorted(all_vaults, key=lambda x: x.scores.vaultScore, reverse=True)

    async def _fetch_from_evm(self) -> List[Vault_EVM]:
        """Fetch vault data from EVM networks"""
        url = "https://blueprint.api.sui-dev.bluefin.io/api/tools/evm/get-vaults"
        async with aiohttp.ClientSession() as session:
            try:
                payload = {
                    "conversationId": self.conversation_id,
                    "userId": self.user_id
                }
                async with session.post(url, json=payload) as response:
                    response.raise_for_status()
                    data = await response.json()
                    vault_response = VaultResponse(**data)
                    return vault_response.data
            except Exception as e:
                raise Exception(f"Failed to fetch EVM vaults: {str(e)}")

    async def _fetch_from_sui(self) -> List[Vault_EVM]:
        """Fetch vault data from Sui network"""
        # TODO: Implement Sui network fetching
        return []

    async def _fetch_from_solana(self) -> List[Vault_EVM]:
        """Fetch vault data from Solana network"""
        # TODO: Implement Solana network fetching
        return []

    def _calculate_score(self, vault: Vault_EVM) -> float:
        """
        Calculate combined score for a vault based on yield and risk.
        
        Args:
            vault: Vault data to score
            
        Returns:
            Combined score
        """
        # Using 7-day APY as yield metric and inverse of vault score as risk metric
        yield_value = vault.apy.total.day7
        risk_value = 100 - vault.scores.vaultScore  # Inverse vault score to represent risk
        return (self.weight_yield * yield_value) - (self.weight_risk * risk_value)

async def get_vaults(conversation_id: str, user_id: str = "default_user") -> VaultResponse:
    """
    Legacy function to maintain compatibility.
    Fetches vaults from EVM network only.
    
    Args:
        conversation_id (str): The unique conversation id
        user_id (str): The unique user id
    """
    system = VaultSourcingSystem(conversation_id=conversation_id, user_id=user_id)
    vaults = await system.fetch_vaults("EVM")
    return VaultResponse(data=vaults)

if __name__ == "__main__":
    async def test_main():
        try:
            # Test the new system
            system = VaultSourcingSystem(
                conversation_id="2a7847a4-098c-4c97-b006-103e161b0b33",
                user_id="1234567890"
            )
            
            # Fetch from all networks
            print("Fetching from all networks...")
            all_vaults = await system.fetch_vaults("ALL")
            if all_vaults:
                print(f"\nFound {len(all_vaults)} vaults in total")
                print(f"Top vault: {all_vaults[0].name} ({all_vaults[0].protocol})")
                print(f"TVL: ${all_vaults[0].tvlUsd}")
                print(f"7-day APY: {all_vaults[0].apy.total.day7}%")
            
            # Test legacy function
            print("\nTesting legacy function...")
            result = await get_vaults(
                conversation_id="2a7847a4-098c-4c97-b006-103e161b0b33",
                user_id="1234567890"
            )
            if result.data:
                print(f"Legacy function returned {len(result.data)} vaults")
                
        except Exception as e:
            print(f"Error: {str(e)}")

    asyncio.run(test_main())
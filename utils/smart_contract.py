import asyncio
from web3 import Web3
from config import Config
from collections import defaultdict
from utils.logger import logger

class SmartContract:
    def __init__(self, token = 'jade'):
        network = Config.network
        self.network_provider = Config.NETWORKS[network]
        self.web3 = Web3(Web3.HTTPProvider(self.network_provider))
        
    async def estimate_gas_price(self):
        return self.web3.eth.gas_price

    async def get_eth_balance(self, address):
        balance = self.web3.eth.get_balance(address)
        return Web3.from_wei(balance, 'ether')

    async def get_token_balance(self, address, tokenAddress):
        
        tokenContract = self.web3.eth.contract(
            address=Web3.to_checksum_address(tokenAddress),
            abi=Config.TOKEN_CONTRACT_ABI
        )
        decimals = tokenContract.functions.decimals().call()
        balance = tokenContract.functions.balanceOf(address).call()
        return balance / pow ( 10, int(decimals))

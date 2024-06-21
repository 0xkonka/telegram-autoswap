import time
from web3 import Web3
from config import Config
from utils.logger import logger
from decimal import Decimal

class SmartContract:
    def __init__(self):
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
        return balance / ( 10 ** int(decimals))
    
    async def get_token_decimal(self, tokenAddress):
        
        tokenContract = self.web3.eth.contract(
            address=Web3.to_checksum_address(tokenAddress),
            abi=Config.TOKEN_CONTRACT_ABI
        )
        decimals = tokenContract.functions.decimals().call()
        return int(decimals)
    
    async def allowance(self, tokenAddress, sender, receiver):
        tokenContract = self.web3.eth.contract(
            address=Web3.to_checksum_address(tokenAddress),
            abi=Config.TOKEN_CONTRACT_ABI
        )
        logger.debug(f"Get {sender} 's allowance to {receiver}")
        allowance = tokenContract.functions.allowance(sender, receiver).call()
        decimals = tokenContract.functions.decimals().call()
        return allowance / ( 10 ** int(decimals))
    
    async def approve(self, private_key, sender, receiver, tokenAddress, amount):
        logger.debug(f"Approve {amount} amounts to {receiver}")
        estimated_gas_price = await self.estimate_gas_price()
        gas_price = int(Decimal(estimated_gas_price) * Decimal(1.2))
        tokenContract = self.web3.eth.contract(
            address=Web3.to_checksum_address(tokenAddress),
            abi=Config.TOKEN_CONTRACT_ABI
        )
        decimals = tokenContract.functions.decimals().call()
        tx = tokenContract.functions.approve(receiver, int(Decimal(amount) * Decimal(10) ** Decimal(int(decimals)))).build_transaction({
            'from': sender,
            'gas': 2000000,
            'gasPrice': gas_price,
            'nonce': self.web3.eth.get_transaction_count(sender),
        })
        signed_tx = self.web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        return tx_hash.hex()

    async def swapExactTokensForTokens(self, private_key , account, routerAddress , path , amountIn):
        logger.debug(f"swapExactTokensForTokens: {account} swap {amountIn} tokens")
        estimated_gas_price = await self.estimate_gas_price()
        gas_price = int(Decimal(estimated_gas_price) * Decimal(1.2))
        tokenContract = self.web3.eth.contract(
            address=Web3.to_checksum_address(path[0]),
            abi=Config.TOKEN_CONTRACT_ABI
        )
        routerContract = self.web3.eth.contract(
            address=Web3.to_checksum_address(routerAddress),
            abi=Config.ROUTER_CONTRACT_ABI
        )
        
        decimals = tokenContract.functions.decimals().call()
        deadline = int(time.time()) + 60 * 20
        
        tx = routerContract.functions.swapExactTokensForTokens(
            int(Decimal(amountIn) * ( Decimal(10) ** Decimal(int(decimals)))),
            0,
            path,
            account,
            deadline
        ).build_transaction({
            'from': account,
            'gas': 2000000,
            'gasPrice': gas_price,
            'nonce': self.web3.eth.get_transaction_count(account),
        })
        signed_tx = self.web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex()

    async def swapTokensForExactTokens(self, private_key , account, routerAddress , path , amountIn,  amountOut):
        logger.debug(f"swapTokensForExactTokens : {account} swap {amountOut} tokens")
        estimated_gas_price = await self.estimate_gas_price()
        gas_price = int(Decimal(estimated_gas_price) * Decimal(1.2))
        base_token_contract = self.web3.eth.contract(
            address=Web3.to_checksum_address(path[1]),
            abi=Config.TOKEN_CONTRACT_ABI
        )
        routerContract = self.web3.eth.contract(
            address=Web3.to_checksum_address(routerAddress),
            abi=Config.ROUTER_CONTRACT_ABI
        )
        
        base_decimals = base_token_contract.functions.decimals().call()
        deadline = int(time.time()) + 60 * 20
        
        tx = routerContract.functions.swapTokensForExactTokens(
            int(Decimal(amountOut) * ( Decimal(10) ** Decimal(int(base_decimals)))),
            amountIn,
            path,
            account,
            deadline
        ).build_transaction({
            'from': account,
            'gas': 2000000,
            'gasPrice': gas_price,
            'nonce': self.web3.eth.get_transaction_count(account),
        })
        signed_tx = self.web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex()

import asyncio
from utils.smart_contract import SmartContract
from utils.db import wallets_collection
from web3 import Web3
from config import Config
from utils.wallet import get_wallet
from utils.logger import logger
import time
import aiohttp
from decimal import Decimal

async def get(session, url, params=None):
    async with session.get(url, params=params) as response:
        return await response.json()

async def post(session, url, data):
    async with session.post(url, json=data) as response:
        return await response.json()
    
async def evm_get_tokens():
    try:
        
        async with aiohttp.ClientSession() as session:
            response = await get(session, Config.EVM_TRADE_API)
            print(f'response : {response}')
            return response
    except Exception as e:
        logger.error(f"GET action failed: {e}")
        return f"GET action failed: {e}"

# async def evm_trade(amount):

#     try:
#         data = {
#             'amount': amount,
#         }
#         async with aiohttp.ClientSession() as session:
#             response = await post(session, Config.EVM_TRADE_API, data)
#             print(f'response : {response}')
#             return response
    
#     except Exception as e:
#         logger.error(f"EVM Trade failed: {e}")
#         return f"EVM Trade failed: {e}"

async def swapExactTokensForTokens(user_id, amountIn):
    
    wallet = await get_wallet(user_id)
    baseToken = "0x9848422A708960e6f416f719006328077Ad1816A"
    quoteToken = "0xB88b5F025382AaDaC2F87A01f950223e7Ee68a1b"
    routerAddr = '0xC532a74256D3Db42D0Bf7a0400fEFDbad7694008'
    
    sc = SmartContract()
    token_balance = await sc.get_token_balance(wallet.evm_wallet_address, baseToken)

    allowance = await sc.allowance(baseToken , wallet.evm_wallet_address, routerAddr)
    if allowance < int(amountIn) :
        tx_hash = await sc.approve(wallet.evm_private_key, wallet.evm_wallet_address, routerAddr, baseToken, token_balance)
        await asyncio.sleep(5)
        logger.debug(f"Approved {token_balance} token placed with tx hash: {tx_hash}")

    if wallet:
        try:
            tx_hash = await sc.swapExactTokensForTokens(wallet.evm_private_key, wallet.evm_wallet_address, routerAddr, [baseToken, quoteToken], amountIn )
            return {"message": f"{amountIn} Based token swapped to Quote Token , tx: {tx_hash}"}
        except ValueError as e:
            if 'already known' in str(e):
                logger.warning(f"Transaction already known, retrying...")
                await asyncio.sleep(5)  # Wait a bit before retrying
            else:
                logger.error(f"Network Error: {str(e)}")
                return {"message": "Network Error"}
    return {"message": "Wallet not found"}

async def swapTokensForExactTokens(user_id, amountOut):
    
    wallet = await get_wallet(user_id)
    baseToken = "0x9848422A708960e6f416f719006328077Ad1816A"
    quoteToken = "0xB88b5F025382AaDaC2F87A01f950223e7Ee68a1b"
    routerAddr = '0xC532a74256D3Db42D0Bf7a0400fEFDbad7694008'
    
    sc = SmartContract()
    base_token_balance = await sc.get_token_balance(wallet.evm_wallet_address, baseToken)
    base_token_decimals = await sc.get_token_decimal(baseToken)
    quote_token_decimals = await sc.get_token_decimal(quoteToken)

    allowance = await sc.allowance(quoteToken , wallet.evm_wallet_address, routerAddr)
    routerContract = sc.web3.eth.contract(
            address=Web3.to_checksum_address(routerAddr),
            abi=Config.ROUTER_CONTRACT_ABI
        )
    amountsIn = routerContract.functions.getAmountsIn(int(Decimal(amountOut) * ( Decimal(10) ** Decimal(int(base_token_decimals)))), [quoteToken, baseToken]).call()
    amountIn = amountsIn[0]
    
    if allowance < int(amountIn) / ( 10 ** int(quote_token_decimals)) :
        tx_hash = await sc.approve(wallet.evm_private_key, wallet.evm_wallet_address, routerAddr, quoteToken, base_token_balance)
        await asyncio.sleep(5)
        logger.debug(f"Approved {base_token_balance} token placed with tx hash: {tx_hash}")

    if wallet:
        try:
            tx_hash = await sc.swapTokensForExactTokens(wallet.evm_private_key, wallet.evm_wallet_address, routerAddr, [quoteToken, baseToken], amountIn, amountOut )
            return {"message": f"{int(amountIn) / ( 10 ** int(quote_token_decimals))} Quote token swapped to {amountOut} Base Token, tx: {tx_hash}"}
        except ValueError as e:
            if 'already known' in str(e):
                logger.warning(f"Transaction already known, retrying...")
                await asyncio.sleep(5)  # Wait a bit before retrying
            else:
                logger.error(f"Network Error: {str(e)}")
                return {"message": "Network Error"}
    return {"message": "Wallet not found"}

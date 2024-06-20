import asyncio
from utils.smart_contract import SmartContract
from utils.db import wallets_collection
from web3 import Web3
from config import Config
from utils.wallet import get_wallet
from utils.logger import logger
import time
import aiohttp

async def get(session, url, params=None):
    async with session.get(url, params=params) as response:
        return await response.json()

async def post(session, url, data):
    async with session.post(url, json=data) as response:
        return await response.json()
    
async def solana_get_tokens():
    try:
        
        async with aiohttp.ClientSession() as session:
            response = await get(session, Config.SOLANA_TRADE_API)
            print(f'response : {response}')
            return response
    except Exception as e:
        logger.error(f"GET action failed: {e}")
        return f"GET action failed: {e}"

async def solana_trade(amount):

    try:
        data = {
            'amount': amount,
        }
        async with aiohttp.ClientSession() as session:
            response = await post(session, Config.SOLANA_TRADE_API, data)
            print(f'response : {response}')
            return response
    
    except Exception as e:
        logger.error(f"Solana Trade failed: {e}")
        return f"Solana Trade failed: {e}"

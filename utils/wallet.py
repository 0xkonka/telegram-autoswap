from pydantic import BaseModel
from utils.db import wallets_collection
from web3 import Web3
from eth_account import Account
import secrets
from solders.keypair import Keypair
import base58
from typing import Optional

class Wallet(BaseModel):
    user_id: int
    evm_private_key: Optional[str] = None
    solana_private_key: Optional[str] = None
    evm_wallet_address: Optional[str] = None
    solana_wallet_address: Optional[str] = None

async def create_evm_wallet(user_id: int) -> Wallet:
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    print("SAVE BUT DO NOT SHARE THIS:", private_key)
    acct = Account.from_key(private_key)

    wallet_data = await wallets_collection.find_one({"user_id": user_id})

    if wallet_data:
        # Update existing wallet
        result = await wallets_collection.update_one(
            {"user_id": user_id},
            {"$set": {"evm_private_key": private_key, "evm_wallet_address": acct.address}}
        )
        if result.modified_count > 0:
            wallet_data.update(evm_private_key=private_key, evm_wallet_address=acct.address)
    else:
        # Insert new wallet
        wallet_data = Wallet(user_id=user_id, evm_private_key=private_key, evm_wallet_address=acct.address)
        await wallets_collection.insert_one(wallet_data.dict())

    return wallet_data if isinstance(wallet_data, Wallet) else Wallet(**wallet_data)

async def import_evm_wallet(user_id: int, private_key: str) -> Wallet:
    acct = Account.from_key(private_key)
    wallet_data = await wallets_collection.find_one({"user_id": user_id})
    
    if wallet_data:
        # Update existing wallet
        result = await wallets_collection.update_one(
            {"user_id": user_id},
            {"$set": {"evm_private_key": private_key, "evm_wallet_address": acct.address}}
        )
        if result.modified_count > 0:
            wallet_data.update(evm_private_key=private_key, evm_wallet_address=acct.address)
    else:
        # Insert new wallet
        wallet_data = Wallet(user_id=user_id, evm_private_key=private_key, evm_wallet_address=acct.address)
        await wallets_collection.insert_one(wallet_data.dict())
    
    return wallet_data if isinstance(wallet_data, Wallet) else Wallet(**wallet_data)

async def import_solana_wallet(user_id: int, private_key: str) -> Wallet:
    
    private_key_bytes = base58.b58decode(private_key)
    keypair = Keypair.from_bytes(private_key_bytes)
    public_key = keypair.pubkey()
    public_key_base58 = base58.b58encode(bytes(public_key)).decode('utf-8')
    print("Public Key:", public_key_base58)
    
    wallet_data = await wallets_collection.find_one({"user_id": user_id})
    
    if wallet_data:
        # Update existing wallet
        result = await wallets_collection.update_one(
            {"user_id": user_id},
            {"$set": {"solana_private_key": private_key, "solana_wallet_address": public_key_base58}}
        )
        if result.modified_count > 0:
            wallet_data.update(solana_private_key=private_key, solana_wallet_address=public_key_base58)
    else:
        # Insert new wallet
        wallet_data = Wallet(user_id=user_id, solana_private_key=private_key, solana_wallet_address=public_key_base58)
        await wallets_collection.insert_one(wallet_data.dict())
    
    return wallet_data if isinstance(wallet_data, Wallet) else Wallet(**wallet_data)

async def get_wallet(user_id: int) -> Wallet:
    wallet = await wallets_collection.find_one({"user_id": user_id})
    return Wallet(**wallet) if wallet else None


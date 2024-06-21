# utils/balance.py

from utils.smart_contract import SmartContract
from utils.wallet import get_wallet
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from solana.rpc.types import TokenAccountOpts
from trade.evm import evm_get_tokens
from trade.solana import solana_get_tokens
from config import Config

async def get_gas_balance(wallet):
    
    eth_balance = 0
    sol_balance = 0
    
    if not wallet:
        return "Wallet not found. Please create or import a wallet first."
    if wallet.evm_wallet_address :
        eth_balance = await SmartContract().get_eth_balance(wallet.evm_wallet_address)
    
    # client = AsyncClient("https://api.mainnet-beta.solana.com")
    if wallet.solana_wallet_address :
        client = AsyncClient(Config.NETWORKS[Config.solana_network])
        
        pubkey = Pubkey.from_string(wallet.solana_wallet_address)
        
        response = await client.get_balance(pubkey)
        balance = response.value
        sol_balance = balance / 1_000_000_000
        await client.close()
        
    return (
        f"EVM Wallet Address: {wallet.evm_wallet_address}\n"
        f"ETH Balance: {eth_balance} ETH\n"
        f"Solana Wallet Address: {wallet.solana_wallet_address}\n"
        f"SOL Balance: {sol_balance} SOL\n"
    )

async def get_evm_trade_token_balance(wallet):
    
    evm_base_balance = 0
    evm_quote_balance = 0
    sol_base_balance = 0
    sol_quote_balance = 0
    
    if not wallet:
        return "Wallet not found. Please create or import a wallet first."
    
    # evm_tokens = await evm_get_tokens()
    # solana_tokens = await solana_get_tokens()
    
    baseToken = "0x9848422A708960e6f416f719006328077Ad1816A"
    quoteToken = "0xB88b5F025382AaDaC2F87A01f950223e7Ee68a1b"
    
    if wallet.evm_wallet_address :
        evm_base_balance = await SmartContract().get_token_balance(wallet.evm_wallet_address , baseToken)
        evm_quote_balance = await SmartContract().get_token_balance(wallet.evm_wallet_address , quoteToken)
    
    # if wallet.solana_wallet_address :
    #     client = AsyncClient(Config.NETWORKS[Config.solana_network])
        
    #     token_accounts = await client.get_token_accounts_by_owner(
    #         Pubkey.from_string(wallet.solana_wallet_address),
    #         TokenAccountOpts(program_id='TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA')
    #     )
        
    #     print(f'token_accounts: {token_accounts}')
        
    #     if not token_accounts['result']['value']:
    #         return 0

    #     token_account_pubkey = token_accounts['result']['value'][0]['pubkey']
    #     token_balance = await client.get_token_account_balance(Pubkey.from_string(token_account_pubkey))
        
    #     print(f'token_balance: {token_balance}')

    #     sol_base_balance = token_balance['result']['value']['uiAmount']

    #     await client.close()
        
    return (
        f"Wallet: {wallet.evm_wallet_address}\n"
        f"base token: {baseToken} \n"
        f"base token Balance: {evm_base_balance} \n"
        f"quote token: {quoteToken} \n"
        f"quote token Balance: {evm_quote_balance} \n"
        # f"Solana Wallet Address: {wallet.solana_wallet_address}\n"
        # f"SOL base spl Balance: {sol_base_balance} \n"
        # f"SOL quote spl Balance: {sol_quote_balance} \n"
    )


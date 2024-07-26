# utils/balance.py

from solana.rpc.api import Client as SolanaClient
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import get_associated_token_address

# from solana.rpc.async_api import AsyncClient
# from solana.rpc.types import TokenAccountOpts

from utils.smart_contract import SmartContract
from utils.wallet import get_wallet
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
    
    if not wallet:
        return "Wallet not found. Please create or import a wallet first."
    
    baseToken = "0x9848422A708960e6f416f719006328077Ad1816A"
    quoteToken = "0xB88b5F025382AaDaC2F87A01f950223e7Ee68a1b"
    
    if wallet.evm_wallet_address :
        evm_base_balance = await SmartContract().get_token_balance(wallet.evm_wallet_address , baseToken)
        evm_quote_balance = await SmartContract().get_token_balance(wallet.evm_wallet_address , quoteToken)
    
    return (
        f"Wallet: {wallet.evm_wallet_address}\n"
        f"base token: {baseToken} \n"
        f"base token Balance: {evm_base_balance} \n"
        f"quote token: {quoteToken} \n"
        f"quote token Balance: {evm_quote_balance} \n"
    )


async def get_sol_trade_token_balance(wallet):
    
    sol_base_balance = 0
    sol_quote_balance = 0
    
    if not wallet:
        return "Wallet not found. Please create or import a wallet first."
    
    solanaBaseToken = "Eu38fqibuYsWPR9hQYN7dP5hSu7a2BzdyQEwHUtGNCfE"
    solanaQuoteToken = "So11111111111111111111111111111111111111112"
    
    if wallet.solana_wallet_address :
        
        user_pubkey = Pubkey.from_string(wallet.solana_wallet_address)
        base_mint_pubkey = Pubkey.from_string(solanaBaseToken)
        quote_mint_pubkey = Pubkey.from_string(solanaQuoteToken)
        payer_keypair = Keypair.from_base58_string(Config.SOLANA_PRIVATE_KEY)

        client = SolanaClient(Config.NETWORKS[Config.solana_network])
        base_spl_client = Token(
            conn=client,
            pubkey=base_mint_pubkey,
            program_id=TOKEN_PROGRAM_ID,
            payer=payer_keypair,
        )
        
        quote_spl_client = Token(
            conn=client,
            pubkey=quote_mint_pubkey,
            program_id=TOKEN_PROGRAM_ID,
            payer=payer_keypair,
        )
        
        try :
            user_token_account = (
                base_spl_client.get_accounts_by_owner(
                    owner=user_pubkey, commitment=None, encoding="base64"
                )
                .value[0]
                .pubkey
            )
            sol_base_balance = base_spl_client.get_balance(user_token_account).value.amount
        
        except Exception as e:
            sol_base_balance = 0
            
        try :
            user_token_account = (
                quote_spl_client.get_accounts_by_owner(
                    owner=user_pubkey, commitment=None, encoding="base64"
                )
                .value[0]
                .pubkey
            )
            sol_quote_balance = quote_spl_client.get_balance(sol_quote_balance).value.amount
        
        except Exception as e:
            sol_quote_balance = 0
            
        
        print(f'balance: {sol_base_balance}')
        
    return (
        f"Solana Wallet Address: {wallet.solana_wallet_address}\n"
        f"base token: {solanaBaseToken} \n"
        f"SOL base spl Balance: {sol_base_balance} \n"
        f"base token: {solanaQuoteToken} \n"
        f"SOL quote spl Balance: {sol_quote_balance} \n"
    )


from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config
from utils.wallet import create_evm_wallet, import_solana_wallet, get_wallet
from utils.logger import logger
from utils.balance import get_gas_balance
from web3 import Web3
from statics.text import *
from utils.smart_contract import SmartContract

user_states = {}

def solana_wallet_handler(bot: Client):

    @bot.on_callback_query(filters.regex("change_wallet_solana"))
    async def on_import_wallet(client: Client, callback_query: CallbackQuery):
        user_id = callback_query.from_user.id
        logger.debug(f"Importing solana wallet for user {user_id}")
        try:
            await callback_query.message.reply("Please provide the solana private key:")
            user_states[user_id] = "awaiting_private_key_solana"
        except Exception as e:
            logger.error(f"Error importing wallet: {e}")
            
    @bot.on_callback_query(filters.regex("import_wallet_solana"))
    async def on_import_wallet(client: Client, callback_query: CallbackQuery):
        user_id = callback_query.from_user.id
        logger.debug(f"Importing solana wallet for user {user_id}")
        try:
            await callback_query.message.reply("Please provide the solana private key:")
            user_states[user_id] = "awaiting_private_key_solana"
        except Exception as e:
            logger.error(f"Error importing wallet: {e}")

    @bot.on_message(filters.text & filters.create(lambda _, __, msg: user_states.get(msg.from_user.id) == "awaiting_private_key_solana"))
    async def handle_private_key(client: Client, message: Message):
        user_id = message.from_user.id
        private_key = message.text
        logger.debug(f"Received solana private key from user {user_id}")
        try:
            wallet = await import_solana_wallet(user_id, private_key)
            balance_message = await get_gas_balance(wallet)
            await message.reply(balance_message)
            user_states.pop(user_id, None)
        except Exception as e:
            logger.error(f"Error importing wallet: {e}")

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config
from utils.wallet import create_evm_wallet, import_evm_wallet, get_wallet
from utils.logger import logger
from utils.balance import get_gas_balance
from web3 import Web3
from statics.text import *
from utils.smart_contract import SmartContract

user_states = {}

def evm_wallet_handler(bot: Client):

    @bot.on_callback_query(filters.regex("change_wallet_evm"))
    async def on_change_wallet(client: Client, callback_query: CallbackQuery):
        user_id = callback_query.from_user.id
        logger.debug(f"User {user_id} wants to change wallet")
        try:
            buttons = [
                [InlineKeyboardButton("Create new wallet", callback_data="create_wallet_evm")],
                [InlineKeyboardButton("Import wallet", callback_data="import_wallet_evm")]
            ]
            await callback_query.message.reply("Please choose an option to proceed:", reply_markup=InlineKeyboardMarkup(buttons))
        except Exception as e:
            logger.error(f"Error handling change_wallet: {e}")

    @bot.on_callback_query(filters.regex("create_wallet_evm"))
    async def on_create_wallet(client: Client, callback_query: CallbackQuery):
        user_id = callback_query.from_user.id
        logger.debug(f"Creating wallet for user {user_id}")
        try:
            wallet = await create_evm_wallet(user_id)
            await callback_query.message.reply(
                f"{CRATE_WALLET_MESSAGE} {wallet.evm_private_key}\n"
            )
            await callback_query.message.reply(f"Successfully Added Wallet\n {wallet.evm_wallet_address}")
        except Exception as e:
            logger.error(f"Error creating wallet: {e}")

    @bot.on_callback_query(filters.regex("import_wallet_evm"))
    async def on_import_wallet(client: Client, callback_query: CallbackQuery):
        user_id = callback_query.from_user.id
        logger.debug(f"Importing wallet for user {user_id}")
        try:
            await callback_query.message.reply("Please provide the private key:")
            user_states[user_id] = "awaiting_private_key"
        except Exception as e:
            logger.error(f"Error importing wallet: {e}")

    @bot.on_message(filters.text & filters.create(lambda _, __, msg: user_states.get(msg.from_user.id) == "awaiting_private_key"))
    async def handle_private_key(client: Client, message: Message):
        user_id = message.from_user.id
        private_key = message.text
        logger.debug(f"Received private key from user {user_id}")
        try:
            wallet = await import_evm_wallet(user_id, private_key)
            balance_message = await get_gas_balance(wallet)
            await message.reply(balance_message)
            user_states.pop(user_id, None)
        except Exception as e:
            logger.error(f"Error importing wallet: {e}")

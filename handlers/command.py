from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from utils.balance import get_gas_balance , get_evm_trade_token_balance
from utils.wallet import get_wallet
# from handlers.wallet_evm import proceed_after_wallet_connection
from utils.logger import logger
from statics.text import *

def command_handler(bot: Client):
    
    @bot.on_message(filters.command("evm_wallet"))
    async def start(client: Client, message: Message):
        user_id = message.from_user.id
        logger.debug(f"Received /evm_wallet command from user {user_id}")
        try:
            wallet = await get_wallet(user_id)
            if wallet.evm_wallet_address:
                buttons = [
                    [InlineKeyboardButton("Change Wallet", callback_data="change_wallet_evm")]
                ]
                await message.reply(f"EVM wallet : {wallet.evm_wallet_address}", reply_markup=InlineKeyboardMarkup(buttons))
            else:
                buttons = [
                    [InlineKeyboardButton("Create new wallet", callback_data="create_wallet_evm")],
                    [InlineKeyboardButton("Import wallet", callback_data="import_wallet_evm")]
                ]
                await message.reply(f"EVM wallet : {wallet.evm_wallet_address}",reply_markup=InlineKeyboardMarkup(buttons))
                # await message.reply("Please choose an option to proceed:", reply_markup=InlineKeyboardMarkup(buttons))
        except Exception as e:
            logger.error(f"Error handling /evm_wallet command: {e}")
    @bot.on_message(filters.command("solana_wallet"))
    async def start(client: Client, message: Message):
        user_id = message.from_user.id
        logger.debug(f"Received /solana_wallet command from user {user_id}")
        try:
            wallet = await get_wallet(user_id)
            if wallet.solana_wallet_address:
                buttons = [
                    [InlineKeyboardButton("Change Wallet", callback_data="change_wallet_solana")]
                ]
                await message.reply(f"Solana wallet : {wallet.solana_wallet_address}", reply_markup=InlineKeyboardMarkup(buttons))
            else:
                buttons = [
                    [InlineKeyboardButton("Import Wallet", callback_data="import_wallet_solana")]
                ]
                await message.reply(f"Solana wallet : {wallet.solana_wallet_address}",reply_markup=InlineKeyboardMarkup(buttons))
                # await message.reply("Please choose an option to proceed:", reply_markup=InlineKeyboardMarkup(buttons))
        except Exception as e:
            logger.error(f"Error handling /solana_wallet command: {e}")
    @bot.on_message(filters.command("balance_gas"))
    async def balance_gas(client: Client, message: Message):
        user_id = message.from_user.id
        logger.debug(f"Received /balance_gas command from user {user_id}")
        user_id = message.from_user.id
        wallet = await get_wallet(user_id)
        balance_message = await get_gas_balance(wallet)
        await message.reply(balance_message)
        
    @bot.on_message(filters.command("balance_trade"))
    async def balance_trade(client: Client, message: Message):
        user_id = message.from_user.id
        logger.debug(f"Received /balance_trade command from user {user_id}")
        user_id = message.from_user.id
        wallet = await get_wallet(user_id)
        evm_balance_message = await get_evm_trade_token_balance(wallet)
        await message.reply(evm_balance_message)
        
    @bot.on_message(filters.command("menu"))
    async def menu(client: Client, message: Message):
        user_id = message.from_user.id
        logger.debug(f"Received /menu command from user {user_id}")
        await message.reply(f"{MENU_MESSAGE}")
        
    @bot.on_message(filters.command("trade"))
    async def menu(client: Client, message: Message):
        user_id = message.from_user.id
        logger.debug(f"Received /trade command from user {user_id}")
        buttons = [
            [InlineKeyboardButton("EVM Trade", callback_data="trade_evm")],
            [InlineKeyboardButton("Solana Trade", callback_data="trade_solana")]
        ]
        await message.reply("Choose the network you want to trade:", reply_markup=InlineKeyboardMarkup(buttons))

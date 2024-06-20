import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config
from utils.logger import logger
from web3 import Web3
from trade.evm import evm_trade

amount_states = {}
user_evm_amount = {}

def evm_trade_handler(bot: Client):
    
    @bot.on_callback_query(filters.regex("trade_evm"))
    async def on_auto_trade_evm(client: Client, callback_query: CallbackQuery):
        user_id = callback_query.from_user.id
        logger.debug(f"EnterEVM trade amount for user {user_id}")
        try:
            await callback_query.message.reply("Please enter swap amount:")
            amount_states[user_id] = "awaiting_evm_amount"
        except Exception as e:
            logger.error(f"Error get trading amount: {e}")

    @bot.on_message(filters.text & filters.create(lambda _, __, msg: amount_states.get(msg.from_user.id) == "awaiting_evm_amount"))
    async def handle_evm_amount(client: Client, message: Message):
        user_id = message.from_user.id
        logger.debug(f"Received EVM trade amount for user {user_id}")
        user_evm_amount[user_id] = message.text
        
        buttons = [
            [InlineKeyboardButton("1 hr", callback_data="evm_duration_1")],
            [InlineKeyboardButton("2 hr", callback_data="evm_duration_2")],
            [InlineKeyboardButton("3 hr", callback_data="evm_duration_3")]
        ]
        await message.reply("Please choose an period:", reply_markup=InlineKeyboardMarkup(buttons))
        
    @bot.on_callback_query(filters.regex(r"evm_duration_\d+"))
    async def on_evm_trade(client: Client, callback_query: CallbackQuery):
        
        data_parts = callback_query.data.split('_')
        duration = int(data_parts[2])
        logger.debug(f"User {callback_query.from_user.id} selected {duration} hrs")
        trade_amount = user_evm_amount.get(callback_query.from_user.id)
        
        if int(trade_amount) > 0:
            user_id = callback_query.from_user.id
            logger.debug(f"User {user_id} is trading with {trade_amount}")
            asyncio.create_task(periodic_trade(bot, user_id, trade_amount, duration * 3600))
            # result = await evm_trade(trade_amount)
            # await callback_query.message.reply(result)

# Function to perform the trade periodically
async def periodic_trade(bot, user_id, trade_amount, duration):
    end_time = asyncio.get_event_loop().time() + duration
    while asyncio.get_event_loop().time() < end_time:
        logger.debug(f"User {user_id} is trading with {trade_amount}")
        await bot.send_message(user_id, "Trading...")
        result = await evm_trade(trade_amount)
        # if "failed" in result.lower():
        #     break
        await bot.send_message(user_id, result['message'])
        await bot.send_message(user_id, f"hash: {result['data']['hash1']}")
        await bot.send_message(user_id, f"hash: {result['data']['hash2']}")
        await asyncio.sleep(5)
    logger.debug(f"User {user_id} EVM trading session completed")
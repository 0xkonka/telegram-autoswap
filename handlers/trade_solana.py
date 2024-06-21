import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config
from utils.logger import logger
from trade.solana import solana_trade

user_solana_get_swap_amount_states = {}
user_solana_swap_amount = {}
user_solana_auto_swap_state = {}

def solana_trade_handler(bot: Client):
    
    @bot.on_callback_query(filters.regex("trade_solana"))
    async def on_auto_trade_solana(client: Client, callback_query: CallbackQuery):
        await callback_query.message.delete()
        user_id = callback_query.from_user.id
        logger.debug(f"Enter Solana trade amount for user {user_id}")
        try:
            await callback_query.message.reply("Please enter base swap amount:")
            user_solana_get_swap_amount_states[user_id] = "awaiting_solana_amount"
        except Exception as e:
            logger.error(f"Error getting trading amount: {e}")

    @bot.on_message(filters.text & filters.create(lambda _, __, msg: user_solana_get_swap_amount_states.get(msg.from_user.id) == "awaiting_solana_amount"))
    async def handle_solana_amount(client: Client, message: Message):
        user_id = message.from_user.id
        logger.debug(f"Received Solana trade amount for user {user_id}")
        user_solana_swap_amount[user_id] = message.text
        
        user_solana_get_swap_amount_states[user_id] = "received_evm_base_amount"
        
        buttons = [
            [InlineKeyboardButton("1 hr", callback_data="solana_duration_1")],
            [InlineKeyboardButton("2 hr", callback_data="solana_duration_2")],
            [InlineKeyboardButton("3 hr", callback_data="solana_duration_3")]
        ]
        await message.reply("Please choose a period:", reply_markup=InlineKeyboardMarkup(buttons))
        
    @bot.on_callback_query(filters.regex(r"solana_duration_\d+"))
    async def on_solana_trade(client: Client, callback_query: CallbackQuery):
        user_id = callback_query.from_user.id
        
        await callback_query.message.delete()
        user_solana_auto_swap_state[user_id] = True
        buttons = [
            [InlineKeyboardButton("Stop", callback_data="solana_stop_auto_swap")]
        ]
        await callback_query.message.reply("Auto swap in progress...", reply_markup=InlineKeyboardMarkup(buttons))
        
        data_parts = callback_query.data.split('_')
        duration = int(data_parts[2])
        logger.debug(f"User {callback_query.from_user.id} selected {duration} hrs")
        trade_amount = user_solana_swap_amount.get(callback_query.from_user.id)
        
        if int(trade_amount) > 0:
            logger.debug(f"User {user_id} is trading with {trade_amount}")
            asyncio.create_task(periodic_trade(bot, user_id, trade_amount, duration * 3600))

    @bot.on_callback_query(filters.regex("solana_stop_auto_swap"))
    async def on_solana_stop_auto_swap(client: Client, callback_query: CallbackQuery):
        user_id = callback_query.from_user.id
        await stop_auto_swap(user_id, callback_query.message)

    @bot.on_message(filters.command("stop_solana"))
    async def on_solana_stop_auto_swap_command(client: Client, message: Message):
        user_id = message.from_user.id
        await stop_auto_swap(user_id, message)

async def stop_auto_swap(user_id, message):
    user_solana_auto_swap_state[user_id] = False
    await message.reply("Auto swap stopped")

async def periodic_trade(bot, user_id, trade_amount, duration):
    end_time = asyncio.get_event_loop().time() + duration
    while asyncio.get_event_loop().time() < end_time:
        if not user_solana_auto_swap_state.get(user_id):
            break

        logger.debug(f"User {user_id} is trading with {trade_amount}")
        
        try:
            result = await solana_trade(trade_amount)
            await bot.send_message(user_id, f"tx: {result['data']['hash1']}")
            await bot.send_message(user_id, f"tx: {result['data']['hash2']}")
        except Exception as e:
            logger.error(f"Error during solana_trade: {e}")
            await bot.send_message(user_id, "Error during solana_trade")
        
        await asyncio.sleep(5)
    
    user_solana_auto_swap_state[user_id] = False
    logger.debug(f"User {user_id} solana trading session completed")

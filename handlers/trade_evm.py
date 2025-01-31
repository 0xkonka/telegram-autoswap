import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import Config
from utils.logger import logger
from web3 import Web3
from trade.evm import swapExactTokensForTokens, swapTokensForExactTokens
from utils.balance import get_gas_balance, get_evm_trade_token_balance
from utils.wallet import get_wallet

user_evm_get_swap_amount_states = {}
user_evm_base_trade_amount = {}
user_evm_quote_trade_amount = {}
user_evm_auto_swap_state = {}

def evm_trade_handler(bot: Client):
    
    @bot.on_callback_query(filters.regex("trade_evm"))
    async def on_auto_trade_evm(client: Client, callback_query: CallbackQuery):
        await callback_query.message.delete()
        user_id = callback_query.from_user.id
        wallet = await get_wallet(user_id)
        logger.debug(f"Enter EVM trade amount for user {user_id}")
        try:
            evm_balance_message = await get_evm_trade_token_balance(wallet)
            await callback_query.message.reply(evm_balance_message)
            await callback_query.message.reply("Please enter base token swap amount:")
            user_evm_get_swap_amount_states[user_id] = "awaiting_evm_base_amount"
        except Exception as e:
            logger.error(f"Error getting trading amount: {e}")
            
    @bot.on_message(filters.text & filters.create(lambda _, __, msg: user_evm_get_swap_amount_states.get(msg.from_user.id) == "awaiting_evm_base_amount"))
    async def handle_evm_amount(client: Client, message: Message):
        user_id = message.from_user.id
        logger.debug(f"Received EVM base trade amount for user {user_id}")
        user_evm_base_trade_amount[user_id] = message.text
        
        user_evm_get_swap_amount_states[user_id] = "received_evm_base_amount"
        
        buttons = [
            [InlineKeyboardButton("1 hr", callback_data="evm_duration_1")],
            [InlineKeyboardButton("2 hr", callback_data="evm_duration_2")],
            [InlineKeyboardButton("3 hr", callback_data="evm_duration_3")]
        ]
        await message.reply("Please choose a period:", reply_markup=InlineKeyboardMarkup(buttons))

    @bot.on_callback_query(filters.regex(r"evm_duration_\d+"))
    async def on_evm_trade(client: Client, callback_query: CallbackQuery):
        user_id = callback_query.from_user.id
        
        await callback_query.message.delete()
        user_evm_auto_swap_state[user_id] = True
        buttons = [
            [InlineKeyboardButton("Stop", callback_data="evm_stop_auto_swap")]
        ]
        await callback_query.message.reply("Auto swap in progress...", reply_markup=InlineKeyboardMarkup(buttons))
        
        data_parts = callback_query.data.split('_')
        duration = int(data_parts[2])
        logger.debug(f"User {callback_query.from_user.id} selected {duration} hrs")
        base_trade_amount = user_evm_base_trade_amount.get(callback_query.from_user.id)
        
        if int(base_trade_amount) > 0:
            logger.debug(f"User {user_id} is trading with {base_trade_amount}")
            asyncio.create_task(periodic_trade(callback_query, user_id, base_trade_amount, duration * 3600))
        
    @bot.on_callback_query(filters.regex("evm_stop_auto_swap"))
    async def on_evm_stop_auto_swap(client: Client, callback_query: CallbackQuery):
        user_id = callback_query.from_user.id
        await stop_auto_swap(user_id, callback_query.message)
    @bot.on_message(filters.command("stop_evm"))
    async def on_evm_stop_auto_swap_command(client: Client, message: Message):
        user_id = message.from_user.id
        await stop_auto_swap(user_id, message)

async def stop_auto_swap(user_id, message):
    user_evm_auto_swap_state[user_id] = False
    await message.reply("Auto swap stopped")

# Function to perform the trade periodically
async def periodic_trade(callback_query, user_id, base_trade_amount, duration):
    end_time = asyncio.get_event_loop().time() + duration
    while asyncio.get_event_loop().time() < end_time:
        if not user_evm_auto_swap_state.get(user_id):
            break
        logger.debug(f"User {user_id} is trading with {base_trade_amount}")
        
        try:
            result = await swapExactTokensForTokens(user_id, base_trade_amount)
            await callback_query.message.reply(result['message'])
        except Exception as e:
            logger.error(f"Error during swapExactTokensForTokens: {e}")
            await callback_query.message.reply("Error during swapExactTokensForTokens")
        await asyncio.sleep(7)
        
        if not user_evm_auto_swap_state.get(user_id):
            break
        
        try:
            result = await swapTokensForExactTokens(user_id, base_trade_amount)
            await callback_query.message.reply(result['message'])
        except Exception as e:
            logger.error(f"Error during swapTokensForExactTokens: {e}")
            await callback_query.message.reply("Error during swapTokensForExactTokens")
        await asyncio.sleep(7)
    user_evm_auto_swap_state[user_id] = False

    logger.debug(f"User {user_id} EVM trading session completed")

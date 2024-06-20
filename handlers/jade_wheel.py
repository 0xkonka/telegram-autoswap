from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from utils.logger import logger
from games.jade_wheel_action import manual_bet
from config import Config

def jade_wheel_handler(bot: Client):
    @bot.on_callback_query(filters.regex("game_wheel_manual_spin"))
    async def on_game_wheel_manual_spin(client: Client, callback_query: CallbackQuery):
        logger.debug(f"User {callback_query.from_user.id} selected manual spin")
        buttons = [
            [InlineKeyboardButton("Jade", callback_data="wheel_manual_jade")],
            [InlineKeyboardButton("xJade", callback_data="wheel_manual_xJade")],
            [InlineKeyboardButton("WETH", callback_data="wheel_manual_weth")]
        ]
        await callback_query.message.reply("Which currency do you want to bet", reply_markup=InlineKeyboardMarkup(buttons))
    
    @bot.on_callback_query(filters.regex(r"wheel_manual_(jade|xJade|weth)"))
    async def on_wheel_manual_jade(client: Client, callback_query: CallbackQuery):
        currency = callback_query.data.split("_")[-1]
        logger.debug(f"User {callback_query.from_user.id} selected manual spin {currency} token")

        buttons = []
        bet_amounts = next((amounts for amounts in Config.BET_AMOUNT if currency in amounts), None)

        if bet_amounts:
            for index, betAmount in enumerate(bet_amounts[currency]):
                buttons.append([InlineKeyboardButton(f"{betAmount} {currency}", callback_data=f"spin_manual_{currency}_{index}")])
        
        await callback_query.message.reply(f"Choose the amount you want to bet with {currency}:", reply_markup=InlineKeyboardMarkup(buttons))

    @bot.on_callback_query(filters.regex(r"spin_manual_(jade|xJade|weth)_\d+"))
    async def on_spin(client: Client, callback_query: CallbackQuery):
        
        data_parts = callback_query.data.split('_')
        currency = data_parts[2]
        index = int(data_parts[3])
        bet_amounts = next((amounts for amounts in Config.BET_AMOUNT if currency in amounts), None)
        
        if bet_amounts:
            bet_amount = bet_amounts[currency][index]
            user_id = callback_query.from_user.id
            logger.debug(f"User {user_id} is spinning with {bet_amount} {currency}")
            await callback_query.message.reply("Spinning...")
            result = await manual_bet(bot, user_id, bet_amount, currency)
            await callback_query.message.reply(result)

            buttons = [
                [InlineKeyboardButton("Spin same amount", callback_data=f"spin_manual_{currency}_{index}")],
                [InlineKeyboardButton("Spin different amount", callback_data="game_wheel_manual_spin")]
            ]
            await callback_query.message.reply("Choose your next action:", reply_markup=InlineKeyboardMarkup(buttons))

    @bot.on_callback_query(filters.regex("game_wheel_auto_spin"))
    async def on_game_wheel_auto_spin(client: Client, callback_query: CallbackQuery):
        logger.debug(f"User {callback_query.from_user.id} selected auto spin")
        buttons = [
            [InlineKeyboardButton("5000 xJade autoSpin", callback_data="autospin_5000")],
            [InlineKeyboardButton("15000 xJade autoSpin", callback_data="autospin_15000")],
            [InlineKeyboardButton("25000 xJade autoSpin", callback_data="autospin_25000")]
        ]
        await callback_query.message.reply("Choose the amount you want to bet:", reply_markup=InlineKeyboardMarkup(buttons))

    @bot.on_callback_query(filters.regex(r"autospin_\d+"))
    async def on_auto_spin_options(client: Client, callback_query: CallbackQuery):
        
        data_parts = callback_query.data.split('_')
        currency = data_parts[2]
        index = int(data_parts[3])
        bet_amount = Config.BET_AMOUNT[currency.lower()][index]
        user_id = callback_query.from_user.id
        logger.debug(f"User {user_id} is spinning with {bet_amount} {currency}")
        
        buttons = [
            [InlineKeyboardButton("10 spins", callback_data=f"start_auto_spin_{bet_amount}_10")],
            [InlineKeyboardButton("50 spins", callback_data=f"start_auto_spin_{bet_amount}_50")],
            [InlineKeyboardButton("100 spins", callback_data=f"start_auto_spin_{bet_amount}_100")],
            [InlineKeyboardButton("200 spins", callback_data=f"start_auto_spin_{bet_amount}_200")],
            [InlineKeyboardButton("300 spins", callback_data=f"start_auto_spin_{bet_amount}_300")],
            [InlineKeyboardButton("500 spins", callback_data=f"start_auto_spin_{bet_amount}_500")]
        ]
        await callback_query.message.reply("Choose the number of spins:", reply_markup=InlineKeyboardMarkup(buttons))

    @bot.on_callback_query(filters.regex(r"start_auto_spin_\d+_\d+"))
    async def on_start_auto_spin(client: Client, callback_query: CallbackQuery):
        data = callback_query.data.split('_')
        bet_amount = int(data[2])
        spin_count = int(data[3])
        user_id = callback_query.from_user.id
        logger.debug(f"User {user_id} starting auto spin with {bet_amount} xJade for {spin_count} spins")

        # Perform the auto spin logic here...
        await callback_query.message.reply(f"Started auto spin with {bet_amount} xJade for {spin_count} spins. TX in progress...")

        buttons = [
            [InlineKeyboardButton("Stop", callback_data="stop_auto_spin")],
            [InlineKeyboardButton("Start again", callback_data=f"start_auto_spin_{bet_amount}_{spin_count}")]
        ]
        await callback_query.message.reply("Auto spin in progress. Choose your action:", reply_markup=InlineKeyboardMarkup(buttons))

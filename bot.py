import logging
import asyncio
import sys
from pyrogram import Client, filters, idle
from config import Config
from utils.logger import logger
from utils.smart_contract import SmartContract

logging.getLogger('pyrogram').setLevel(logging.WARNING)

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

bot = Client("wonka_trade_bot", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)

# Import handlers
from handlers.command import command_handler
from handlers.wallet_evm import evm_wallet_handler
from handlers.wallet_solana import solana_wallet_handler
from handlers.trade_evm import evm_trade_handler
from handlers.trade_solana import solana_trade_handler

# Register handlers
command_handler(bot)
evm_wallet_handler(bot)
solana_wallet_handler(bot)
evm_trade_handler(bot)
solana_trade_handler(bot)

# async def main():
#     # Start the bot
#     await bot.start()
#     print("Bot is running")

#     # Keep the bot running
#     await idle()
    
# if __name__ == "__main__":
#     asyncio.run(main())

# async def start_monitoring():
#     sc = SmartContract()
#     await sc.monitor_events()

# if __name__ == "__main__":
#     asyncio.create_task(start_monitoring())
#     bot.run()
    


# async def main():
#     # Create a background task for monitoring events
#     asyncio.create_task(start_monitoring())

#     # Start the bot
#     bot.run()
    
# async def start_monitoring():
#     sc = SmartContract()
#     await sc.monitor_events()

if __name__ == "__main__":
    bot.run()
    # asyncio.run(main())
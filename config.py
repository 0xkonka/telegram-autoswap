import json

class Config:
    network = 'sepolia'
    solana_network = 'solana_mainnet'
    NETWORKS = {
        'base_mainnet': 'https://base.publicnode.com', # 'https://mainnet.base.org'
        'sepolia': 'https://eth-sepolia.g.alchemy.com/v2/mGsqrKffb5Yt_jmlL0UsiyPz8ZT7jBCv',
        'solana_devnet' : 'https://devnet.helius-rpc.com/?api-key=d6fef362-e3c9-414a-995e-95e6578bd8bc',
        'solana_mainnet' : 'https://rpc.ankr.com/solana/1afcaf5033ad295e853ea93c0167f9c724ac22a34f653ef5f818ad21a38e9e97'
    }
    API_ID = 1608993
    API_HASH = "b3f7fa4c1b406018036a5b5f3dca57d2"
    BOT_TOKEN = "7090032780:AAEQwbe53ZegbCau2hUnUy8qRB0_TsdaNbc"
    # BOT_TOKEN = "7287562420:AAFKDYbiOBgjsGXL5i-27g-GDPU6zQiZ-Kc"
    DATABASE_URI = "mongodb+srv://quinnlee1020:4Dm4y1Kdj8gAiecD@cluster0.urm6i4n.mongodb.net/wonkaTelegram"
    
    SOLANA_PRIVATE_KEY = "2UKaqHjSS28pxdziYvnVWd2QY2Jyp4uZmBa8LmuJcQgKLNftFGBVrA9GEHKybWFEwjZqwLwFd9m2Fr3BD5Qjeyoh"
    
    EVM_TRADE_API = 'http://auction.chocolatefactory.gg/api/trade/evm'
    SOLANA_TRADE_API = 'http://auction.chocolatefactory.gg/api/trade/solana'
    
    with open('./abi/token.json', 'r') as abi_file:
        TOKEN_CONTRACT_ABI = json.load(abi_file)
    
    with open('./abi/uniswapRouter.json', 'r') as abi_file:
        ROUTER_CONTRACT_ABI = json.load(abi_file)
    
    # WHEEL_CONTRACT_ADDRESS = {
    #     'base_mainnet': {
    #         'default': {
    #             'address': '0x7a4afB5Ef76f7512f8cD05b5a15a75d2f6DFEC88',
    #             'abi': jadeWheelRNGABI
    #             },
    #         'weth': {
    #             'address': '0x24617Ba900d19536cD4d286a9632776A3201Fb03',
    #             'abi': wethWheelDefABI
    #         }
    #     },
    #     'base_sepolia':  {
    #         'default': '',
    #         'weth': ''
    #     },
    #     'sepolia':  {
    #         'default': {
    #             'address':'0x38bA18b6259C3fe72FD9B2D00B38fAaBC45Be818',
    #             'abi': jadeWheelUnsafeRNGABI
    #             },
    #         'weth': {
    #             'address': '0xFb1D152Dc5b7D5BaE57016554CfAEF31a8a6c5A2',
    #             'abi': wethWheelUnsafeRNGABI
    #             }
    #     }
    # }
    # TOKEN_CONTRACT_ADDRESS = {
    #     'base_mainnet': {
    #         'jade': '0x628c5Ba9B775DACEcd14E237130c537f497d1CC7',
    #         'xjade': '',
    #         'weth': '0x4200000000000000000000000000000000000006'
    #     }, 
    #     'base_sepolia': {
    #         'jade': '0x812a630b4A0C01024Ef47329036C77db24DF4C9A',
    #         'xjade': '0x3C3BfE38936D663934d34baD43881B0FAf77aDB6',
    #         'weth': ''
    #     }, 
    #     'sepolia': {
    #         'jade': '0xa6b7BE1673C4bF0153B2C19f645e4aB566B30317',
    #         'xjade': '',
    #         'weth': '0xfFf9976782d46CC05630D1f6eBAb18b2324d6B14'
    #     }, 
    # }
    # BET_AMOUNT = {
    #     "weth": [0.0088, 0.01, 0.02, 0.03, 0.05, 0.06, 0.08, 0.088],
    #     "jade": [888, 8888, 10000, 15000, 20000, 30000, 50000, 80000],
    #     "xjade": [888, 8888, 10000, 15000, 20000, 30000, 50000, 80000]
    # },
    # AUTO_BET_COUND = [8, 16, 32, 64, 128, 256, 512]






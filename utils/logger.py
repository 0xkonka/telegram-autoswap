import logging

logger = logging.getLogger('jade_roll_bot')
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
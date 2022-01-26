from asyncio import get_event_loop

from gluon import gluon_bot

from config import GLUON


loop = get_event_loop()

try:
    loop.run_until_complete(gluon_bot.start(GLUON))
except:
    loop.close()

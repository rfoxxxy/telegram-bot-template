from bot_template import PROJECT_NAME, config, dp, is_prod, loop, scheduler
from bot_template.core import BotCore

core = BotCore(PROJECT_NAME, is_prod, dp, loop, config, scheduler)

core.start()

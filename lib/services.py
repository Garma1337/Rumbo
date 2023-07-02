# coding: utf-8

from discord import Bot, Intents

from lib.config import Config
from lib.logger import Logger

bot: Bot = Bot(intents=Intents.all())
config: Config = Config.from_file()
logger: Logger = Logger(config)

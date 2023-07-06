# coding: utf-8

from typing import NoReturn

from discord import ApplicationContext, slash_command, Cog, Bot

from commands.coinflip import CoinflipResult, coinflip


class CoinflipCommand(Cog):

    @slash_command(name='coinflip', description='Play a game of coinflip.')
    async def coinflip(self, context: ApplicationContext) -> NoReturn:
        await context.defer()

        coinflip_result: CoinflipResult = await coinflip(context.channel, context.user)

        if coinflip_result.random_side == coinflip_result.selected_side:
            await context.respond('You guessed correctly. Congratulations!')
        else:
            await context.respond('You did not guess correctly. Play again if you want.')


def setup(bot: Bot):
    bot.add_cog(CoinflipCommand())

from random import choice

from discord import Embed, Colour
from discord.ext import commands
from discord.utils import get

from systems.money_system import money_system

from base import BaseCog
from gifs import GIFS
from config import STATUSES, EMOTIONS_COST


class EmotionsCog(BaseCog):

    def create_embed(self, ctx, args, action, gifs, pre):
        msg = f'{ctx.author.mention} {action}'
        has_mention = False

        if len(ctx.message.mentions) > 1:
            return
        elif len(ctx.message.mentions) == 1:
            msg += f' {pre} {ctx.message.mentions[0].mention}'
            has_mention = True

        if has_mention and args[1:]:
            msg += ' и ' + ' '.join(args[1:])
        elif not has_mention and args:
            msg += ' и ' + ' '.join(args)

        embed = Embed(colour=Colour(0x36393f), description=msg)
        embed.set_image(url=choice(gifs))
        return embed

    async def emotions(self, ctx, args, emotion, gifs, s):
        if get(ctx.author.roles, id=STATUSES['VIP_ROLE']):
            money_system.take_money(ctx.author.id, {'energy': EMOTIONS_COST / 2})
        else:
            money_system.take_money(ctx.author.id, {'energy': EMOTIONS_COST})

        return await ctx.send(embed=self.create_embed(ctx, args, emotion, gifs, s))

    @commands.command(aliases=['выпить'])
    async def drink(self, ctx, *args):
        return await self.emotions(ctx, args, 'пьет', GIFS['drink'], 'с')

    @commands.command(aliases=['раздеваться'])
    async def undress(self, ctx, *args):
        return await self.emotions(ctx, args, 'раздевается', GIFS['undress'], 'перед')

    @commands.command(aliases=['весело'])
    async def funny(self, ctx, *args):
        return await self.emotions(ctx, args, 'веселится', GIFS['funny'], 'с')

    @commands.command(aliases=['смущение'])
    async def shiny(self, ctx, *args):
        return await self.emotions(ctx, args, 'смущается', GIFS['shiny'], 'перед')

    @commands.command(aliases=['злость'])
    async def angry(self, ctx, *args):
        return await self.emotions(ctx, args, 'злится', GIFS['angry'], 'на')

    @commands.command(aliases=['шок'])
    async def shock(self, ctx, *args):
        return await self.emotions(ctx, args, 'шокирован', GIFS['shock'], 'от')

    @commands.command(aliases=['грусть'])
    async def sad(self, ctx, *args):
        return await self.emotions(ctx, args, 'грустит', GIFS['sad'], 'с')

    @commands.command(aliases=['любовь'])
    async def love(self, ctx, *args):
        return await self.emotions(ctx, args, 'влюбился', GIFS['love'], 'в')

    @commands.command(aliases=['кусать'])
    async def bite(self, ctx, *args):
        return await self.emotions(ctx, args, 'укусил', GIFS['bite'], '')

    @commands.command(aliases=['лапать'])
    async def paw(self, ctx, *args):
        return await self.emotions(ctx, args, 'лапает', GIFS['paw'], '')

    @commands.command(aliases=['ласкать'])
    async def caress(self, ctx, *args):
        return await self.emotions(ctx, args, 'ласкает', GIFS['caress'], '')

    @commands.command(aliases=['обнять'])
    async def hug(self, ctx, *args):
        return await self.emotions(ctx, args, 'обнимает', GIFS['hug'], '')

    @commands.command(aliases=['поцеловать'])
    async def kiss(self, ctx, *args):
        return await self.emotions(ctx, args, 'целует', GIFS['kiss'], '')

    @commands.command(aliases=['тыкнуть'])
    async def poke(self, ctx, *args):
        return await self.emotions(ctx, args, 'тыкает', GIFS['poke'], 'в')

    @commands.command(aliases=['ударить'])
    async def slam(self, ctx, *args):
        return await self.emotions(ctx, args, 'ударил', GIFS['slam'], '')

from random import randint
from collections import OrderedDict
from datetime import datetime, timedelta

from discord import Member
from discord.ext import commands
from discord.utils import get

from base import BaseCog, strfdelta
from systems.inventory_system import inventory_system
from systems.bonus_system import bonus_system
from systems.money_system import money_system

from embeds.economy import *
from embeds.default import DefaultEmbed
from config import ECONOMY, SHOP, STATUSES, GUILD_ID


class EconomyCog(BaseCog):

    def __init__(self, bot):
        super().__init__(bot)
        self._shop = None
        self.emoji = {}
        self.guild = None

    async def cog_check(self, ctx):
        return ctx.message.channel.id != 601121051795128330

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(GUILD_ID)

        self._shop = OrderedDict(sorted(SHOP['ROLES'].items(), key=lambda k: list(k[1].values())[0], reverse=True))

        for role_id, cost in self._shop.copy().items():
            role = self.guild.get_role(role_id)
            self._shop[role] = self._shop.pop(role_id)

        self.emoji['avasilver'] = get(self.guild.emojis, name='avasilver')
        self.emoji['avagold'] = get(self.guild.emojis, name='avagold')

        fields = [
            {'name': 'role2', 'aliases': ['купон2', 'к2'], 'help': 'role_2', 'brief': 'Передать купон на личную роль 2 дн'},
            {'name': 'role3', 'aliases': ['купон3', 'к3'], 'help': 'role_3', 'brief': 'Передать купон на личную роль 3 дн'},
            {'name': 'role6', 'aliases': ['купон6', 'к6'], 'help': 'role_6', 'brief': 'Передать купон на личную роль 6 дн'},

            {'name': 'bgift', 'aliases': ['бподарок', 'бп'], 'help': 'bgift', 'brief': 'Передать большой подарок'},
            {'name': 'sgift', 'aliases': ['мподарок', 'мп'], 'help': 'sgift', 'brief': 'Передать маленький подарок'},

            {'name': 'batteries', 'aliases': ['батарейка', 'б'], 'help': 'batteries', 'brief': 'Передать батарйки'},
            {'name': 'pillows', 'aliases': ['подушка', 'п'], 'help': 'pillows', 'brief': 'Передать подушки'},

            {'name': 'cakes', 'aliases': ['торт', 'т'], 'help': 'cakes', 'brief': 'Передать тортики'},

        ]

        for field in fields:
            self.give.add_command(commands.Command(self._give_item, **field))

    @commands.command(aliases=['халява'], brief='Получить ежедневный бонус')
    async def everyday(self, ctx):
        author_id = ctx.author.id

        if not bonus_system.has_bonus(author_id, 'silver'):
            today = bonus_system.bonus_date(author_id, 'silver') + timedelta(hours=12)
            td = today - datetime.now().replace(microsecond=0)

            embed = Embed(
                title="Ежедневный бонус",
                description=f"Ты уже получил сегодня ежедневный бонус, тебе осталось `{strfdelta(td)}`",
                colour=Colour(0xffffff)
            )
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/610456153503301632/615261118520360962/image_3840.png"
            )
            return await ctx.send(embed=embed)

        bonus_system.get_bonus(author_id, 'silver')
        bonus_money = ECONOMY['EVERYDAY_BONUS']

        if get(ctx.author.roles, id=STATUSES['VIP_ROLE']):
            bonus_money *= 2

        money_system.add_money(author_id, currency={'silver': bonus_money})
        return await ctx.send(embed=EverydayBonus(bonus_money, self.emoji['avasilver']).embed)

    @commands.command(aliases=['магазин'])
    async def shop(self, ctx):
        embed = Embed(colour=Colour(0xffffff))

        embed.set_author(name="Магазин")
        embed.set_footer(text="!купить [номер]")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/607620198534479883/615273786341589003/image_3263.png"
        )

        for i, role in enumerate(self._shop, 1):
            cost = self._shop[role]

            if role is int or role is None:
                continue

            embed.add_field(
                name=f"№ {i}", value=f"{role.mention} - {cost['silver']} {self.emoji['avasilver']}", inline=False
            )

        return await ctx.send(embed=embed)

    @commands.group(aliases=['продать'])
    async def sell(self, ctx):
        if not ctx.invoked_subcommand:
            msg = ''

            for command in ctx.command.commands:
                msg += f'`{self.bot.command_prefix}{ctx.command.name} {command.name}` - {command.brief}\n'

            await ctx.send(msg)

    @sell.command(aliases=['роль'], brief='Продать купон на личную роль [кол-во дней] [кол-во] ')
    async def role(self, ctx, days: int, cnt: int):
        inventory_system.take_item(ctx.author.id, {f'role_{days}': cnt})

        money = 0
        if days == 2:
            money = 900
        if days == 3:
            money = 1800
        if days == 6:
            money = 3000

        money_system.add_money(ctx.author.id, {'silver': money*cnt})
        return await ctx.send(embed=DefaultEmbed(f'Вы заработали {money*cnt} {self.emoji["avasilver"]}'))

    @commands.group(aliases=['дать'])
    async def give(self, ctx):
        if not ctx.invoked_subcommand:
            msg = ''

            for command in ctx.command.commands:
                msg += f'`{self.bot.command_prefix}{ctx.command.name} {command.name}` - {command.brief}\n'

            return await ctx.send(embed=DefaultEmbed(msg))

    @give.command(aliases=['серебро'], brief="Передать серебро другому участнику")
    async def silver(self, ctx, member: Member, money: int):
        money_system.take_money(ctx.author.id, {'silver': money})
        tax = ECONOMY['TAX']

        if get(ctx.author.roles, id=STATUSES['VIP_ROLE']):
            tax = 1

        money = int((money * (100-tax)) / 100)
        money_system.add_money(member.id, {'silver': money})

        await ctx.send(embed=DefaultEmbed(
            f'Вы передали {member.mention} - {money} {self.emoji["avasilver"]}, комиссия `{tax}%`'
        ))

    @give.command(aliases=['золото'], brief="Передать золото другому участнику")
    async def gold(self, ctx, member: Member, money: int):
        money_system.transact_money(ctx.author.id, member.id, {'gold': money})
        await ctx.send(embed=DefaultEmbed(
            f'Вы передали {member.mention} - {money} {self.emoji["avagold"]}'
        ))

    @sell.command(aliases=['кольцо', 'к'])
    async def ring(self, ctx, cnt: int):
        inventory_system.take_item(ctx.author.id, {'rings': cnt})
        money = 500

        money_system.add_money(ctx.author.id, {'silver': money * cnt})
        return await ctx.send(embed=DefaultEmbed(f'Вы заработали {money*cnt} {self.emoji["avaring"]}'))

    # @sell.command(aliases=['акольцо', 'ак'])
    # async def drings(self, ctx, cnt: int):
    #     inventory_system.take_item(ctx.author.id, {'drings': cnt})
    #     money = 50
    #
    #     money_system.add_money(ctx.author.id, {'gold': money * cnt})
    #     return await ctx.send(embed=DefaultEmbed(f'Вы заработали {money * cnt} {self.emoji["avagold"]}'))
    #
    # @sell.command(aliases=['ркольцо', 'рк'])
    # async def rrings(self, ctx, cnt: int):
    #     inventory_system.take_item(ctx.author.id, {'rrings': cnt})
    #     money = 250
    #
    #     money_system.add_money(ctx.author.id, {'gold': money * cnt})
    #     return await ctx.send(embed=DefaultEmbed(f'Вы заработали {money * cnt} {self.emoji["avagold"]}'))

    async def _give_item(self, ctx, member: Member, money: int):
        currency = ctx.command.help
        inventory_system.take_item(ctx.author.id, {currency: money})
        inventory_system.add_item(member.id, {currency: money})
        await ctx.send(embed=DefaultEmbed(f'Вы передали {member.mention} - x{money}'))

    @commands.command(aliases=['купить'])
    async def buy(self, ctx, number: int):
        try:
            if number <= 0:
                raise IndexError

            role, cost = list(self._shop.items())[number - 1]
        except IndexError:
            return await ctx.send('Нет такой позиции в магазине')

        if not role:
            return await ctx.send('Нет такой роли в магазине')

        if role in ctx.author.roles:
            return await ctx.send('У тебя уже куплена эта роль')

        money_system.take_money(ctx.author.id, cost)

        await ctx.author.add_roles(role)
        return await ctx.send(embed=DefaultEmbed(f'Ты купил себе роль {str(role.mention)}'))

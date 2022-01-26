from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from discord import PermissionOverwrite, Member, Colour
from discord.ext import commands
from discord.utils import get

from systems.inventory_system import inventory_system
from systems.money_system import money_system
from systems.bonus_system import bonus_system

from embeds.shop import DonateShop
from base import BaseCog

from config import DONATE_SHOP, GUILD_ID, STATUSES, LOVE_ROOM_CATEGORY


class DonateCog(BaseCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.donate_shop_embed = None
        self.guild = None
        self.love_room_category = None
        self.emojis = None

        self.premium = None
        self.vip = None
        self.astronaut = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(GUILD_ID)

        self.emojis = {
            'mercdonat': get(self.guild.emojis, name="mercdonat"),
            'mercstar': get(self.guild.emojis, name="mercstar")
        }
        owners = ['<@179302715094990849>', '<@483578366524522507>']
        owners = ' / '.join(owners)

        self.donate_shop_embed = DonateShop(owners, self.emojis)
        self.love_room_category = get(self.guild.categories, id=LOVE_ROOM_CATEGORY)

        self.vip = self.guild.get_role(STATUSES['VIP_ROLE'])

    async def cog_check(self, ctx):
        return ctx.message.channel.id != 601121051795128330

    @commands.command(aliases=['перевод'])
    async def transfer(self, ctx, stars: int):
        if stars < 10:
            return await ctx.send('Обмен от 10 звезд')

        if not money_system.take_money(ctx.author.id, {'donate_money': stars/10}):
            raise commands.CommandError('no money')

        money_system.add_money(ctx.author.id, {'stars': stars})
        return await ctx.send(f'Обменял {int(stars/10)} {self.emojis["mercdonat"]} на {stars} {self.emojis["mercstar"]}')

    @commands.group(aliases=['донат'])
    async def donate(self, ctx):
        if not ctx.invoked_subcommand:
            msg = ''

            for command in ctx.command.commands:
                msg += f'`{self.bot.command_prefix}{ctx.command.name} {command.name}` - {command.brief}\n'

            await ctx.send(msg)

    @donate.command(aliases=['магазин'], brief="Магазин ролей")
    async def shop(self, ctx, *args):
        return await ctx.send(embed=self.donate_shop_embed.embed)

    @donate.command(aliases=['купить'], brief='Покупка роли из магазина за донат валюту')
    async def buy(self, ctx, position: int):
        if position < 1 or position > 10:
            return await ctx.send('Нет такой позиции в магазине')

        money_system.take_money(ctx.author.id, {'donate_money': DONATE_SHOP[position-1]})

        if 1 <= position <= 6:
            return await self.add_roles(ctx, position)

        if position in [7, 8]:
            return await self.love_room(ctx, position)

        if position in [9, 10]:
            return await self.private_role(ctx, position)

    async def add_roles(self, ctx, position):
        days = timedelta(days=7)
        now = datetime.now().replace(microsecond=0)

        if position in [1, 3, 5]:
            days = timedelta(days=30)

        role = self.astronaut
        bonus_type = 'astronaut'

        if position in [1, 2]:
            bonus_type = 'premium'
            role = self.premium
        elif position in [3, 4]:
            bonus_type = 'vip'
            role = self.vip

        for b_type in ['premium', 'vip', 'astronaut']:
            if bonus_type == b_type and bonus_system.has_privilegies(ctx.author.id, b_type):
                dt = bonus_system.get_privilegies_date(ctx.author.id, bonus_type)
                bonus_system.inc_privilegies(ctx.author.id, b_type, dt + days)
                return await ctx.send(f'Вы продлили `{role}`')

        await ctx.author.remove_roles(self.premium, self.vip, self.astronaut)
        await ctx.author.add_roles(role)

        bonus_system.delete_row(ctx.author.id)
        bonus_system.buy_privilegies(ctx.author.id, role.id, now + days, bonus_type)
        return await ctx.send(f'Вы купили `{str(role)}`')

    async def private_role(self, ctx, position):
        role = await self.guild.create_role()
        inventory_system.add_personal_role(role.id, 30 if position == 9 else 7)
        bonus_system.add_role(ctx.author.id, role.id)
        await ctx.author.add_roles(role)
        return await ctx.send(
            'Вы купили личную роль, используйте команду `!роль`, чтобы узнать список доступных команд'
        )

    @commands.group(aliases=['роль'])
    async def role(self, ctx):
        if not ctx.invoked_subcommand:
            msg = ''

            for command in ctx.command.commands:
                msg += f'`{self.bot.command_prefix}{ctx.command.name} {command.name}` - {command.brief}\n'

            await ctx.send(msg)

    @role.command(aliases=['цвет'], brief='Изменить цвет роли')
    @commands.cooldown(1, 60, commands.BucketType.member)
    async def colour(self, ctx, role_id: int, _hex: str):
        try:
            _hex0x = int(_hex, 16)
        except:
            return await ctx.send('Честно сказать, цвет так себе')

        role = self.guild.get_role(role_id)
        premium_role = bonus_system.get_role(ctx.author.id, role_id)

        if not role or not premium_role:
            return await ctx.send('Нет такой роли')

        await role.edit(colour=Colour(_hex0x))
        return await ctx.send('Цвет роли был изменен')

    @role.command(aliases=['забрать'], brief='Забирает личную роль у человека')
    @commands.cooldown(1, 60, commands.BucketType.member)
    async def take(self, ctx, role_id: int, member: Member):
        role = self.guild.get_role(role_id)
        premium_role = bonus_system.get_role(ctx.author.id, role_id)

        if not role or not premium_role:
            return await ctx.send('Нет такой роли')

        if role not in member.roles:
            return await ctx.send('У него нет этой роли')

        bonus_system.add_slot(ctx.author.id, role_id)
        await member.remove_roles(role)
        return await ctx.send('Снял с него роль')

    @role.command(aliases=['дать'], brief='Выдает личную роль человеку')
    @commands.cooldown(1, 60, commands.BucketType.member)
    async def give(self, ctx, role_id: int, member: Member):
        role = self.guild.get_role(role_id)
        premium_role = bonus_system.get_role(ctx.author.id, role_id)

        if premium_role['slots'] == premium_role['max_slots']:
            return await ctx.send('У вас закончились слоты для выдачи этой роли')

        if role in member.roles:
            return await ctx.send('У него уже есть эта роль')

        bonus_system.del_slot(ctx.author.id, role_id)
        await member.add_roles(role)
        return await ctx.send('Выдал ему роль')

    @role.command(aliases=['название'], brief='Изменить название роли')
    @commands.cooldown(1, 60, commands.BucketType.member)
    async def name(self, ctx, role_id: int, *args):
        if not args:
            return await ctx.send('Название не может быть пустым')

        role_name = ' '.join(args)

        if len(role_name) > 30:
            return await ctx.send('Название не больше 30 символов')

        role = self.guild.get_role(role_id)
        premium_role = bonus_system.get_role(ctx.author.id, role_id)

        if not role or not premium_role:
            return await ctx.send('Нет такой роли')

        await role.edit(name=role_name)
        return await ctx.send('Название роли было изменено')

    async def love_room(self, ctx, position):
        love_room = bonus_system.get_love_room(ctx.author.id)
        now = datetime.now()

        if love_room:
            now = love_room['expiration_date']

        dt = now + relativedelta(weeks=1)

        if position == 7:
            dt = now + relativedelta(months=1)

        if love_room:
            bonus_system.inc_love_room(ctx.author.id, dt)
            return await ctx.send('Вы продлили доступ лаврумы')

        overwrites = {
            self.guild.default_role: PermissionOverwrite(connect=False, read_messages=False),
            ctx.author: PermissionOverwrite(read_messages=True, connect=True)
        }

        nick = ctx.author.nick if ctx.author.nick else ctx.author.display_name
        vc = await self.love_room_category.create_voice_channel(nick, overwrites=overwrites, user_limit=2)

        bonus_system.buy_love_room(ctx.author.id, vc.id, dt)
        return await ctx.send(
            'Спасибо за покупку, ваша комната создана, отправьте `!loveroom` / `!лаврум` чтобы узнать команды'
        )

    @commands.group(aliases=['лаврум'])
    async def loveroom(self, ctx):
        if not ctx.invoked_subcommand:
            if not ctx.message.mentions:
                msg = ''

                for command in ctx.command.commands:
                    msg += f'`{self.bot.command_prefix}{ctx.command.name} {command.name}` - {command.brief}\n'
                msg += f'`{self.bot.command_prefix}{ctx.command.name} @link` - Добавить/Удалить из румы участника\n'

                return await ctx.send(msg)

            if len(ctx.message.mentions) > 1:
                raise commands.CommandError('no mention')

            member = ctx.message.mentions[0]

            if member == ctx.author:
                return await ctx.send('Вы уже и так прописаны в лавруму')

            love_room = bonus_system.get_love_room(ctx.author.id)

            if not love_room:
                return await ctx.send('У вас нет лаврумы')

            vc_id = love_room['love_room_id']
            vc = ctx.guild.get_channel(vc_id)
            members_in = [overwrite for overwrite in vc.overwrites if type(overwrite) == Member]
            nick = ctx.author.nick if ctx.author.nick else ctx.author.display_name

            if any(m for m in members_in if m.id == member.id):
                await vc.set_permissions(member, overwrite=None)
                await vc.edit(name=nick)

                return await ctx.send('Вы удалили участника из лаврумы')

            if len(members_in) == 2:
                return await ctx.send('Вы не можете добавить еще одного участника')

            nick = member.nick if member.nick else member.display_name

            await vc.set_permissions(member, overwrite=PermissionOverwrite(connect=True, read_messages=True))
            await vc.edit(name=f'{vc.name} ❤ {nick}')

            return await ctx.send(f'Добавил в лавруму {member.mention}')

    @loveroom.command(aliases=['закрыть'], brief='Закрыть лавруму')
    async def lock(self, ctx, *args):
        return await self._lock(ctx, False)

    @loveroom.command(aliases=['открыть'], brief='Открыть лавруму')
    async def unlock(self, ctx, *args):
        return await self._lock(ctx)

    async def _lock(self, ctx, lock=True):
        love_room = bonus_system.get_love_room(ctx.author.id)

        if not love_room:
            return await ctx.send('У вас нет лаврумы')

        vc = ctx.guild.get_channel(love_room['love_room_id'])
        await vc.set_permissions(
            ctx.guild.default_role, overwrite=PermissionOverwrite(read_messages=lock, connect=False)
        )

        if lock:
            return await ctx.send('Лаврума открыта')
        return await ctx.send('Лаврума закрыта')

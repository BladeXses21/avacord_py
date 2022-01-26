from random import randint, choice

from discord import Colour, Member
from discord.ext import commands
from discord.utils import get

from systems.inventory_system import inventory_system
from systems.money_system import money_system

from embeds.default import DefaultEmbed
from embeds.inventory import InventoryEmbed
from base import BaseCog, required_args, send_dm

from config import GUILD_ID


class InventoryCog(BaseCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.guild = None
        self.emojis = {}
        self._items = {
            'silver': 40,
            'batteries': 20,
            'rings': 15,
            'sgift': 7,
            'cakes': 1,
            'role': 3,
            'bgift': 2,
            'gold': 2,
            'activity': 5
        }

    async def cog_check(self, ctx):
        return ctx.message.channel.id != 601121051795128330

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(GUILD_ID)
        emojis = self.guild.emojis

        self.emojis['avasilver'] = get(emojis, name="avasilver")
        self.emojis['avagold'] = get(emojis, name="avagold")
        self.emojis['avacoffe'] = get(emojis, name="avacoffe")
        self.emojis['avarole2'] = get(emojis, name="avarole2")
        self.emojis['avarole3'] = get(emojis, name="avarole3")
        self.emojis['avarole6'] = get(emojis, name="avarole6")
        self.emojis['avacake'] = get(emojis, name="avacake")
        self.emojis['avacake'] = get(emojis, name="avacake")
        self.emojis['avafortune'] = get(emojis, name="avafortune")
        self.emojis['avagift'] = get(emojis, name="avagift")
        self.emojis['avaactivity'] = get(emojis, name="avaactivity")
        self.emojis['avaring'] = get(emojis, name="avaring")
        self.emojis['avafishki'] = get(emojis, name="avafishki")

    @commands.command(aliases=['инвентарь'])
    async def inventory(self, ctx, *args):
        if len(ctx.message.mentions) == 1:
            member = ctx.message.mentions[0]
        else:
            member = ctx.author

        inventory = inventory_system.get_inventory(member.id)
        return await ctx.send(embed=InventoryEmbed(member, ctx, inventory, self.emojis).embed)

    @commands.command(aliases=['личнаяроль'])
    @required_args(3)
    async def privaterole(self, ctx, *args):
        try:
            role_num = int(args[0])

            if role_num not in [2, 3, 6]:
                return await ctx.send('Неправильный номер купона')

            _hex0x = int(args[1], 16)
            role_name = ' '.join(args[2:])

            if len(role_name) > 15:
                return await ctx.send('Название роли должно быть меньше 15 символов')
        except:
            return await ctx.send('Неправильные циферки')

        if not inventory_system.take_item(ctx.author.id, {f'role_{role_num}': 1}):
            return await ctx.send('У вас нет такого купона')

        role = await ctx.guild.create_role(name=role_name, colour=Colour(_hex0x), mentionable=True)
        await ctx.author.add_roles(role)
        inventory_system.add_personal_role(role.id, role_num)
        return await ctx.send(f'Выдал роль на {role_num}дн {role.mention}')

    @commands.command(aliases=['торт'])
    @commands.cooldown(1, 900, type=commands.BucketType.member)
    async def cake(self, ctx, member: Member):
        try:
            inventory_system.take_item(ctx.author.id, {'cakes': 1})
        except commands.CommandError as ex:
            self.cake.reset_cooldown(ctx)
            raise ex
        await member.edit(nick="Ты в тортике")
        await send_dm(member, f'{str(member)} Кинул в тебя тортиком')
        embed = DefaultEmbed(f'Ты кинул тортик в {member.mention}')
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/607620198534479883/615961138802196481/image_1517.png"
        )
        embed.set_footer(text="Чтобы кинуть торт пропиши !cake @link")
        return await ctx.send(embed=embed)

    @commands.command(aliases=['кофе', 'cofe'])
    @commands.cooldown(1, 2, type=commands.BucketType.member)
    async def coffee(self, ctx, *args):
        try:
            cnt = int(args[0])
        except:
            cnt = 1

        inventory_system.take_item(ctx.author.id, {'batteries': cnt})
        money_system.add_money(ctx.author.id, {'energy': cnt*70})
        return await ctx.send(embed=DefaultEmbed(f'Вы получили {cnt*70} энергии'))

    def drop_item(self, items):
        return choice([k for k, v in items.items() for _ in range(v)])

    @commands.command(aliases=['фортуна'])
    @commands.cooldown(1, 2, type=commands.BucketType.member)
    async def fortune(self, ctx):
        inventory_system.take_item(ctx.author.id, {'sgift': 1})

        silver = randint(10, 500)
        money_system.add_money(ctx.author.id, {'silver': silver})

        embed = DefaultEmbed(f'Ты прокрутил колесо фортуны и тебе выпало **{silver}** {self.emojis["avasilver"]}')
        embed.set_author(name="Колесо фортуны")
        embed.set_footer(text=str(ctx.author), icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/607620198534479883/616272691585875975/image_1796.png"
        )
        return await ctx.send(embed=embed)

    @commands.command(aliases=['подарок'])
    @commands.cooldown(1, 2, type=commands.BucketType.member)
    async def bgift(self, ctx):
        inventory_system.take_item(ctx.author.id, {'bgift': 1})
        item = self.drop_item(self._items)
        msg = ''

        if item == 'silver':
            silver = randint(1, 100)
            money_system.add_money(ctx.author.id, {'silver': silver})
            msg = f'В подарке ты нашел {silver} {self.emojis["avasilver"]}'
        elif item == 'gold':
            cnt = self.drop_item({
                6: 10,
                3: 35,
                1: 55
            })
            money_system.add_money(ctx.author.id, {item: cnt})
            msg = f'В подарке ты нашел {cnt} {self.emojis["avagold"]}'
        elif item in 'role':
            cnt = self.drop_item({
                6: 10,
                3: 35,
                2: 55
            })
            inventory_system.add_item(ctx.author.id, {f'role_{cnt}': 1})
            msg = f'В подарке ты нашел {self.emojis[f"avarole{cnt}"]}'
        elif item == 'batteries':
            cnt = self.drop_item({
                4: 10,
                2: 35,
                1: 55
            })
            inventory_system.add_item(ctx.author.id, {item: cnt})
            msg = f'В подарке ты нашел {cnt} {self.emojis["avacoffe"]}'
        elif item == 'sgift':
            cnt = self.drop_item({
                3: 10,
                2: 35,
                1: 55
            })
            inventory_system.add_item(ctx.author.id, {item: cnt})
            msg = f'В подарке ты нашел {cnt} {self.emojis["avafortune"]}'
        elif item == 'cakes':
            cnt = self.drop_item({
                3: 30,
                1: 70
            })
            inventory_system.add_item(ctx.author.id, {item: cnt})
            msg = f'В подарке ты нашел {cnt} {self.emojis["avacake"]}'
        elif item == 'bgift':
            cnt = self.drop_item({
                5: 10,
                2: 35,
                1: 55
            })
            inventory_system.add_item(ctx.author.id, {item: cnt})
            msg = f'В подарке ты нашел {cnt} {self.emojis["avagift"]}'
        elif item == 'activity':
            cnt = randint(30, 200)
            money_system.add_activity(ctx.author.id, cnt)
            msg = f'В подарке ты нашел {cnt} {self.emojis["avaactivity"]}'
        elif item == 'rings':
            inventory_system.add_item(ctx.author.id, {'rings': 1})
            msg = f'В подарке ты нашел 1 {self.emojis["avaring"]}'
        else:
            from gluon import gluon_logger
            gluon_logger.info(f'Неизвестная вещь {item}')

        embed = DefaultEmbed(msg)
        embed.set_author(name="Открытие подарка")
        embed.set_footer(text=str(ctx.author), icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/607620198534479883/616272169605005332/image_21.png"
        )
        return await ctx.send(embed=embed)

from discord import Embed, Member
from discord.ext import commands

from base import BaseCog
from systems.bonus_system import bonus_system
from systems.admin_system import admin_system
from systems.money_system import money_system
from systems.profile_system import profile_system
from systems.inventory_system import inventory_system

from config import OWNERS, ADMIN_ROLE, MODERATOR_ROLE


class OwnersCog(BaseCog):

    @commands.command()
    @commands.has_role(OWNERS['OWNER_ROLE'])
    async def dellove(self, ctx, vc: int):
        bonus_system.del_love_room(love_room_id=vc)
        return await ctx.send('Лаврума удалена')

    @commands.command()
    @commands.has_role(OWNERS['OWNER_ROLE'])
    async def delactive(self, ctx):
        money_system.del_activty()
        return await ctx.send('Активность обнулена')

    @commands.command()
    @commands.has_role(OWNERS['OWNER_ROLE'])
    async def delrole(self, ctx, role_id: int):
        inventory_system.del_role(role_id)
        return await ctx.send('Личная роль удалена')

    @commands.command('эмодзи')
    @commands.has_role(OWNERS['OWNER_ROLE'])
    async def guild_emojis(self, ctx, *args):
        msg = ''
        for emoji in ctx.guild.emojis:
            if not emoji.managed and emoji.available:
                msg += f'{str(emoji)} - `{emoji.id}`\n'

            if len(msg) > 1000:
                await ctx.send(msg)
                msg = ''

        return await ctx.send(msg)

    @commands.command()
    @commands.has_any_role(OWNERS['OWNER_ROLE'], ADMIN_ROLE, MODERATOR_ROLE)
    async def reports(self, ctx, *args):
        embed = Embed()

        for row in profile_system.top_reports:
            member = ctx.guild.get_member(row['member_id'])

            if not member:
                continue

            embed.add_field(name="Участник", value=f"{member.mention} - {row['reports_cnt']}")
        return await ctx.send(embed=embed)

    @commands.command()
    async def delwarn(self, ctx, *args):
        if ctx.author.id not in [179302715094990849, 607618056537112657]:
            return

        await ctx.send('Запускаю шарманку')
        n = 0

        role = ctx.guild.get_role(OWNERS['WARN_ROLE'])

        for member in role.members:
            await member.remove_roles(role)
            n += 1

        admin_system.remove_all()
        await ctx.send(f'{ctx.author.mention} Дело сделано, снято `{n}`')

    @commands.Cog.listener()
    async def on_ready(self):
        for field in list(money_system.fields)[1:]:
            self.bot.add_command(
                commands.Command(self.add_currency, name=f"ad{field}", checks=[commands.has_role(OWNERS['OWNER_ROLE'])])
            )
            self.bot.add_command(
                commands.Command(self.del_currency, name=f"del{field}", checks=[commands.has_role(OWNERS['OWNER_ROLE'])])
            )

        for field in list(inventory_system.fields)[1:]:
            self.bot.add_command(
                commands.Command(self.add_item, name=f'adi{field}', checks=[commands.has_role(OWNERS['OWNER_ROLE'])])
            )
            self.bot.add_command(
                commands.Command(self.del_item, name=f'deli{field}', checks=[commands.has_role(OWNERS['OWNER_ROLE'])])
            )

    async def add_item(self, ctx, member: Member, money: int):
        item_type = ctx.command.name.split('adi')[-1]
        inventory_system.add_item(member.id, {item_type: money})
        await ctx.send(f'Отдал ему {item_type} `{money}`')

    async def del_item(self, ctx, member: Member, money: int):
        item_type = ctx.command.name.split('deli')[-1]
        inventory_system.take_item(member.id, {item_type: money})
        await ctx.send(f'Забрал у него `{money}`')

    async def del_currency(self, ctx, member: Member, money: int):
        currency = ctx.command.name.split('del')[-1]
        money_system.take_to_zero(member.id, currency={currency: money})
        await ctx.send(f'Забрал у него `{money}`')

    async def add_currency(self, ctx, member: Member, money: int):
        currency = ctx.command.name.split('ad')[-1]
        money_system.add_money(member.id, {currency: money})
        await ctx.send(f'Отдал ему {currency} `{money}`')

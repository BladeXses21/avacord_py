from datetime import datetime, timedelta

from discord import Member
from discord.ext import commands

from embeds.default import DefaultEmbed
from base import BaseCog, strfdelta
from systems.inventory_system import inventory_system
from systems.profile_system import profile_system
from systems.bonus_system import bonus_system

from config import STATUSES


class StatusesCog(BaseCog):

    @commands.command(aliases=['картинка'])
    @commands.has_role(STATUSES['VIP_ROLE'])
    @commands.cooldown(1, 4, type=commands.BucketType.member)
    async def img(self, ctx, img_url: str):
        profile_system.set_img_url(ctx.author.id, img_url)
        return await ctx.send(embed=DefaultEmbed('Картинка установлена на профиль'))

    @commands.command(aliases=['онлайн'])
    @commands.has_role(STATUSES['VIP_ROLE'])
    async def online(self, ctx, member: Member):
        for vc in ctx.guild.voice_channels:
            if member in vc.members:
                return await ctx.send(embed=DefaultEmbed(f'Пользователь в `{str(vc)}`'))
        return await ctx.send(embed=DefaultEmbed('Пользователя нет ни в одном войсе'))

    @commands.command(aliases=['кольцо'])
    @commands.has_role(STATUSES['VIP_ROLE'])
    async def circle(self, ctx, *args):
        member_id = ctx.author.id
        inventory = inventory_system.get_inventory(member_id)

        if inventory['rings'] != 0:
            return await ctx.send(embed=DefaultEmbed('У тебя уже есть кольца'))

        if not bonus_system.has_bonus(member_id, 'rings'):
            today = bonus_system.bonus_date(member_id, 'rings') + timedelta(hours=12)
            td = today - datetime.now().replace(microsecond=0)
            return await ctx.send(embed=DefaultEmbed(f'Кольцо уже выдал, следующее через: `{strfdelta(td)}`'))

        inventory_system.add_item(member_id, {'rings': 1})
        bonus_system.get_bonus(member_id, 'rings')
        return await ctx.send(embed=DefaultEmbed('Выдал тебе кольца'))

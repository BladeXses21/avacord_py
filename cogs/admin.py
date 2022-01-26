from json import loads
from random import randint
from datetime import datetime, timedelta

from discord import Member
from discord.ext import commands
from discord.utils import get

from systems.profile_system import profile_system
from systems.admin_system import admin_system

from base import send_dm, BaseCog

from embeds.default import DefaultEmbed
from embeds.invalid import InvalidEmbed
from embeds.report import ReportEmbed
from embeds.ban import BanEmbed
from embeds.mute import *
from embeds.warn import *

from config import ADMIN, GUILD_ID, OWNER_ROLE, ADMIN_ROLE, MINI_GAMES


class MutesCog(BaseCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.guild = self.bot.get_guild(GUILD_ID)
        self.mute_role = None
        self.mute_channel = None

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(GUILD_ID)
        self.mute_role = guild.get_role(ADMIN['MUTE_ROLE'])
        self.mute_channel = guild.get_channel(ADMIN['MUTE_CHANNEL'])

    @commands.command(aliases=['мутчат', 'мч'])
    @commands.has_any_role(*ADMIN['MUTE_ROLES'])
    async def mutet(self, ctx, member: Member, mins: int, *args):
        now = datetime.now().replace(microsecond=0)
        mute_date = now + timedelta(minutes=mins)

        if not args:
            return await ctx.send(embed=DefaultEmbed('Укажите причину мута'))

        reason = ' '.join(args)

        if self.mute_role in member.roles:
            return await ctx.send(embed=DefaultEmbed('У пользователя уже есть мут'))

        admin_system.delete_mute(member.id)
        admin_system.add_mute(member.id, ctx.author.id, reason, mute_date)

        dt = now + timedelta(hours=7)
        mute_date += timedelta(hours=7)

        await member.remove_roles(ctx.guild.get_role(ADMIN['WARN_ROLE']))
        admin_system.delete_warn(member.id)
        await member.add_roles(self.mute_role, reason='!mute')
        await self.mute_channel.send(embed=MuteEmbed(ctx, member, reason, dt, mute_date).embed)

        try:
            dm = await member.create_dm()
            await dm.send(embed=MuteDMEmbed(ctx, reason, mute_date).embed)
        except:
            pass
        return await ctx.send(embed=DefaultEmbed(f'Выдал ему мут'))

    @commands.command(aliases=['мутвойс', 'мв'])
    @commands.has_any_role(*ADMIN['MUTE_ROLES'])
    async def mutev(self, ctx, member: Member, mins: int, *args):
        now = datetime.now().replace(microsecond=0)
        mute_date = now + timedelta(minutes=mins)

        if not args:
            return await ctx.send(embed=DefaultEmbed('Укажите причину мута'))

        reason = ' '.join(args)

        try:
            await member.edit(mute=True, reason=f'!mutev {str(ctx.author)}')
        except:
            return await ctx.send(embed=DefaultEmbed('Пользователь не в войсе'))

        admin_system.delete_server_mute(member.id)
        admin_system.add_server_mute(member.id, ctx.author.id, reason, mute_date)

        dt = now + timedelta(hours=7)
        mute_date += timedelta(hours=7)

        await member.remove_roles(ctx.guild.get_role(ADMIN['WARN_ROLE']))
        admin_system.delete_warn(member.id)
        await self.mute_channel.send(embed=MuteEmbed(ctx, member, reason, dt, mute_date).embed)

        try:
            dm = await member.create_dm()
            await dm.send(embed=MuteDMEmbed(ctx, reason, mute_date).embed)
        except:
            pass
        return await ctx.send(embed=DefaultEmbed(f'Выдал ему мут'))

    @commands.command(aliases=['размут'])
    @commands.has_any_role(*ADMIN['UNMUTE_ROLES'])
    async def unmutet(self, ctx, member: Member):
        if not admin_system.has_mute(member.id):
            return await ctx.send(embed=DefaultEmbed('У пользователя нет мута'))

        await member.remove_roles(self.mute_role)
        await send_dm(member, f'Вы были размучены пользователем `{ctx.message.author}`')

        admin_system.delete_mute(member.id)
        return await ctx.send(embed=DefaultEmbed(f'Размутил'))

    @commands.command(aliases=['размутв'])
    @commands.has_any_role(*ADMIN['UNMUTE_ROLES'])
    async def unmutev(self, ctx, member: Member):
        if not admin_system.has_server_mute(member.id):
            return await ctx.send(embed=DefaultEmbed('У пользователя нет мута'))

        try:
            await member.edit(mute=False)
            await send_dm(member, f'Вы были размучены пользователем `{ctx.message.author}`')
            admin_system.delete_server_mute(member.id)
        except:
            return await ctx.send(embed=DefaultEmbed('Челика нет в войсе'))
        return await ctx.send(embed=DefaultEmbed(f'Размутил'))


class AdminCog(BaseCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.invalid_role = None
        self.warn_role = None
        self.warn_channel = None
        self.invalid_channel = None
        self.report_channel = None

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(GUILD_ID)
        self.invalid_role = guild.get_role(ADMIN['INVALID_ROLE'])
        self.warn_role = guild.get_role(ADMIN['WARN_ROLE'])
        self.warn_channel = guild.get_channel(ADMIN['WARN_CHANNEL'])
        self.invalid_channel = guild.get_channel(ADMIN['INVALID_CHANNEL'])
        self.report_channel = guild.get_channel(ADMIN['REPORT_CHANNEL'])

    @commands.command()
    @commands.has_any_role(OWNER_ROLE, ADMIN_ROLE, MINI_GAMES['MENTOR_ROLE_ID'])
    async def say(self, ctx, args):
        content = ctx.message.content

        if content.startswith("!say https://discord.gg/"):
            return await ctx.send(content.strip('!say '))

        json = loads(content.strip('!say '))

        if json.get('thumbnail', None):
            json['thumbnail'] = {'url': json['thumbnail']}
        if json.get('image', None):
            json['image'] = {'url': json['image']}

        return await ctx.send(embed=Embed.from_dict(json))

    @commands.command(aliases=['варн'])
    @commands.has_any_role(*ADMIN['WARN_ROLES'])
    async def warn(self, ctx, member: Member, reason: str, *args):
        reason += ' ' + ' '.join(args)

        if not admin_system.create_warn(member.id, ctx.author.id, reason):
            return await ctx.send(embed=DefaultEmbed('У человека уже есть предупреждение'))

        dt = datetime.now().replace(microsecond=0) + timedelta(hours=7)

        await self.warn_channel.send(embed=WarnEmbed(ctx, member, reason, dt).embed)
        await member.add_roles(self.warn_role)

        try:
            dm = await member.create_dm()
            await dm.send(embed=WarnDMEmbed(ctx, reason).embed)
        except:
            pass
        return await ctx.send(embed=DefaultEmbed(f'Выдал ему `{str(self.warn_role)}`'))

    @commands.command(aliases=['снятьварн'])
    @commands.has_any_role(*ADMIN['UNWARN_ROLES'])
    async def unwarn(self, ctx, member: Member):
        if self.warn_role not in member.roles:
            return await ctx.send(embed=DefaultEmbed('Невозможно снять варн, у человека нет ни одного варна'))

        admin_system.delete_warn(member.id)
        await member.remove_roles(self.warn_role)
        await send_dm(member, f'С вас снято предупреждение пользователем `{str(ctx.author)}`')
        return await ctx.send(embed=DefaultEmbed('Варн был снят'))

    @commands.command(aliases=['инвалид'])
    @commands.has_any_role(*ADMIN['INVALID_ROLES'])
    async def invalid(self, ctx, member: Member, reason: str, *args):
        reason += ' ' + ' '.join(args)
        now = datetime.now().replace(microsecond=0) + timedelta(hours=7)

        await member.add_roles(self.invalid_role)
        await ctx.send(embed=DefaultEmbed(f'Выдал ему роль {str(self.invalid_role)}'))
        await send_dm(
            member, f'Вам выдана роль `{str(self.invalid_role)}` от {ctx.message.author}\nпричина: `{reason}`'
        )
        return await self.invalid_channel.send(embed=InvalidEmbed(ctx, member, reason, now).embed)

    @commands.command(aliases=['снятьинвал'])
    @commands.has_any_role(*ADMIN['UNINVAL_ROLES'])
    async def uninval(self, ctx, member: Member):
        await member.remove_roles(self.invalid_role)
        await send_dm(member, f'`{ctx.message.author}` снял вам роль {str(self.invalid_role)}')
        return await ctx.send(embed=DefaultEmbed(f'Снял роль `{str(self.invalid_role)}` с {member.mention}'))

    @commands.command(aliases=['бан'])
    @commands.has_any_role(*ADMIN['BAN_ROLES'])
    async def ban(self, ctx, member: Member, reason: str, *args):
        reason += ' ' + ' '.join(args)

        if not admin_system.add_ban_time(ctx.author.id):
            return await ctx.send(embed=DefaultEmbed(
                'Ты уже 5 раз использовал команду за 24ч, тебе не жалко людей, которых ты уже забанил?'
                ' не буду я никого банить *ТЬФУ*'
            ))

        admin_system.add_ban(member.id, ctx.author.id, reason)

        try:
            dm = await member.create_dm()
            await dm.send(embed=BanEmbed(ctx, reason).embed)
        except:
            await ctx.send(embed=DefaultEmbed('У челика лс закрыто'))

        await ctx.send(embed=DefaultEmbed(f'Ну что? Ты доволен? Теперь `{str(member)}` забанен'))
        await member.ban(reason=reason)

    @commands.command(aliases=['репорт'])
    async def report(self, ctx, *args):
        try:
            request_id = int(args[0])
        except:
            request_id = None

        if get(ctx.author.roles, id=ADMIN['REPORT_ACCEPT_ROLE']) and request_id:
            report = admin_system.get_report(request_id)

            if not report:
                return await ctx.send(embed=DefaultEmbed('Нет такой заявки'))

            msg = await self.report_channel.fetch_message(report['msg_id'])

            embed = msg.embeds[0]
            embed.color = 0x1e240
            embed.add_field(name='Принял', value=f"{ctx.author.mention}")

            member = ctx.guild.get_member(report['from_id'])

            await send_dm(member, f'`{ctx.author}` Принял ваш репорт, номер: `{report["request_id"]}`')
            await ctx.message.delete()
            admin_system.delete_report(report['request_id'])
            return await msg.edit(embed=embed)

        if len(ctx.message.mentions) != 1:
            return await ctx.send('!report / !репорт @линк [причина]')

        member = ctx.message.mentions[0]
        reason = ' '.join(args[1:])
        request_id = randint(100000, 999999)

        created_time = ctx.message.created_at.replace(microsecond=0) + timedelta(hours=3)

        msg = await self.report_channel.send(embed=ReportEmbed(ctx, member, reason, request_id, created_time).embed)
        admin_system.create_report(member.id, ctx.author.id, reason, request_id, created_time, msg.id)
        profile_system.add_report(member.id)
        return await ctx.send(embed=DefaultEmbed('Ваш репорт был отправлен'))

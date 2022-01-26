from discord import Member, Embed, Colour
from discord.ext import commands

from base import has_mention, BaseCog

from config import GUILD_ID, ROLES, ADMIN_ROLE, MENTOR_ROLE, HELPER_ROLE, EVENTER_ROLE, EVENTMEMBER_ROLE


class RoleIDCommand(commands.Command):

    def __init__(self, role_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role_id = role_id

    async def invoke(self, ctx):
        ctx.role_id = self.role_id
        await super().invoke(ctx)


class RolesCog(BaseCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.guild = None
        self.embed = Embed(colour=Colour(0xffffff))

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(GUILD_ID)

        for role_id, cmds in ROLES['ROLES'].items():
            for cmd in cmds:
                self.bot.add_command(RoleIDCommand(role_id, func=self.everyone_role, name=cmd))

        for role_id, cmds in ROLES['MODERATION_ROLES'].items():
            for cmd in cmds:
                self.bot.add_command(RoleIDCommand(role_id, func=self.moder_role, name=cmd))

        for role_id, cmds in ROLES['EVENTER_ROLES'].items():
            for cmd in cmds:
                self.bot.add_command(RoleIDCommand(role_id, func=self.eventer_role, name=cmd))

        self.bot.add_command(RoleIDCommand(HELPER_ROLE, func=self.adm_mentor, name='support', aliases=['саппорт']))
        self.bot.add_command(RoleIDCommand(ROLES['GLOVE'], func=self.adm_mentor, name='glove', aliases=['перчатка']))
        self.bot.add_command(RoleIDCommand(EVENTER_ROLE, func=self.adm_mentor, name='eventer', aliases=['ивентер']))
        self.bot.add_command(RoleIDCommand(EVENTMEMBER_ROLE, func=self.everyone_role, name='event', aliases=['ивент']))

    @commands.cooldown(1, 10, type=commands.BucketType.member)
    async def everyone_role(self, ctx, *args):
        return await self.add_role(ctx, ctx.author)

    @commands.has_any_role(*ROLES['MODERATION_ROLE'])
    async def moder_role(self, ctx, member: Member):
        return await self.add_role(ctx, member)

    @commands.has_any_role(*ROLES['EVENTER_ROLE'])
    @has_mention()
    async def eventer_role(self, ctx, member: Member):
        return await self.add_role(ctx, member)

    @commands.has_any_role(ADMIN_ROLE, MENTOR_ROLE)
    async def adm_mentor(self, ctx, member: Member):
        return await self.add_role(ctx, member)

    async def add_role(self, ctx, member):
        role = self.guild.get_role(ctx.role_id)

        if role in member.roles:
            await member.remove_roles(role)
            self.embed.description = f'Ты перестал быть {role.mention}'
            self.embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/610455053081378834/615271254198321230/image_3261.png"
            )

            return await ctx.send(embed=self.embed)

        await member.add_roles(role)
        self.embed.description = f'Теперь ты {role.mention}'
        self.embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/607620198534479883/616023795064373429/image_3179.png"
        )
        await ctx.send(embed=self.embed)

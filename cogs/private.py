from pickle import load, dump
from os.path import exists

from discord import PermissionOverwrite, Member
from discord.ext import commands, tasks
from discord.utils import get

from base import BaseCog
from embeds.private import TextChannelEmbed

from config import GUILD_ID, PRIVATE_START_ROOM_ID, STATUSES


class PrivatesCog(BaseCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.start_channel = None
        self.guild = None
        self.category = None
        self.premium_role = None
        self.room_admins = self.load_room_admins()

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(GUILD_ID)
        self.start_channel = self.guild.get_channel(PRIVATE_START_ROOM_ID)
        self.category = get(self.guild.categories, id=self.start_channel.category_id)
        self.premium_role = self.guild.get_role(STATUSES['VIP_ROLE'])

        self.start_loop.start()

    @commands.command(aliases=['демо'])
    async def demo(self, ctx):
        if self.premium_role not in ctx.author.roles:
            return await ctx.send(f'Только для {self.premium_role.mention}')

        if self.room_admins.get(ctx.author.id, None) is None:
            return await ctx.send('Вы должны находиться в приватной руме')

        vc_id = self.room_admins[ctx.author.id]['vc']

        tc = self.guild.get_channel(self.room_admins[ctx.author.id]['tc'])

        schema = f'https://discordapp.com/channels/{GUILD_ID}/{vc_id}'
        return await tc.send(schema)

    @commands.command(aliases=['позвать'])
    async def invite(self, ctx, member: Member):
        if self.premium_role not in ctx.author.roles:
            return await ctx.send(f'Только для {self.premium_role.mention}')

        if self.room_admins.get(ctx.author.id, None) is None:
            return await ctx.send('Вы должны находиться в приватной руме')

        tc = self.guild.get_channel(self.room_admins[ctx.author.id]['tc'])
        await tc.set_permissions(member, overwrite=PermissionOverwrite(read_messages=True, send_messages=True))
        return await ctx.send('Выдал ему права на текстовый чат')

    @commands.command(aliases=['пбан'])
    async def pban(self, ctx, member: Member):
        if ctx.author.id not in self.room_admins:
            return await ctx.send(f'{ctx.author.mention} **Ты не создатель приватной румы!**')

        if member.id in [179302715094990849, 607618056537112657]:
            return

        room_channel = self.guild.get_channel(self.room_admins[ctx.author.id]['vc'])

        if self.room_admins[ctx.author.id].get('tc', None):
            tc = self.guild.get_channel(self.room_admins[ctx.author.id]['tc'])
            await tc.set_permissions(member, overwrite=None)

        if member in room_channel.members:
            await member.move_to(None)

        await room_channel.set_permissions(member, overwrite=PermissionOverwrite(connect=False))
        return await ctx.send(f'{ctx.author.mention}, пользователь кикнут')

    def load_room_admins(self):
        if not exists('room_admins.pkl'):
            return {}

        try:
            with open('room_admins.pkl', 'rb') as f:
                return load(f)
        except:
            return {}

    def save_room_admins(self):
        with open('room_admins.pkl', 'wb') as f:
            dump(self.room_admins, f)

    @tasks.loop(seconds=1)
    async def start_loop(self):
        await self.delete_empty_room()
        await self.delete_text_ch()
        await self.create_channel()

        self.save_room_admins()

    async def delete_empty_room(self):
        for channel in self.category.voice_channels:
            if channel == self.start_channel:
                continue

            if not channel.members:
                self.delete_from_admins(channel.id)
                await channel.delete()

    async def delete_text_ch(self):
        tcs = []

        for k, v in self.room_admins.items():
            if v.get('tc', None):
                tcs.append(v['tc'])

        for tc in self.category.text_channels:
            if tc.id not in tcs:
                await tc.delete()

    def delete_from_admins(self, channel_id):
        keys = list(self.room_admins.keys())

        for k in keys:
            if self.room_admins[k]['vc'] == channel_id:
                del self.room_admins[k]
                break

    async def create_channel(self):
        for member in self.start_channel.members:
            channel = await self.category.create_voice_channel(f'Домик #{member.discriminator}', user_limit=2)

            self.room_admins.update({member.id: {'vc': channel.id}})

            if self.premium_role in member.roles:
                overwrites = {
                    self.guild.default_role: PermissionOverwrite(read_messages=False, send_messages=False),
                    member: PermissionOverwrite(read_messages=True, send_messages=True)
                }

                tc = await self.category.create_text_channel(f'Домик #{member.discriminator}', overwrites=overwrites)

                await tc.send(content=member.mention, embed=TextChannelEmbed().embed)
                self.room_admins[member.id].update({'tc': tc.id})

            await channel.set_permissions(member, overwrite=PermissionOverwrite(manage_channels=True))
            await member.move_to(channel)

        self.save_room_admins()

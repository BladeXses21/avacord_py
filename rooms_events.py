import inspect
import pickle
from asyncio import sleep
from os.path import exists

from discord import PermissionOverwrite
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get

from embeds import games
from base import BaseCog, required_args

from config import GUILD_ID, EVENT_START_ROOM_ID, EVENTER_ROLE, MENTOR_ROLE, EVENTMEMBER_ROLE, OWNER_ROLE


class EventCog(BaseCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.guild = None
        self.category = None
        self.create_channel_room = None
        self.eveter = None
        self.mentor = None
        self.eventmember = None
        self.event_rooms = self.load_events()

    def load_events(self):
        if not exists('events.pkl'):
            return {}

        with open('events.pkl', 'rb') as f:
            return pickle.load(f)

    def save_events(self):
        with open('events.pkl', 'wb') as f:
            return pickle.dump(self.event_rooms, f)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.add_roles(self.eventmember)

    @commands.command(aliases=['eventall'])
    @commands.has_role(OWNER_ROLE)
    async def eventmember_all(self, ctx, *args):
        members = ctx.guild.members
        percentage = 5
        percentage_complete = 0
        x = int(len(members) * percentage / 100)

        msg = await ctx.send(f'`{percentage_complete}% Complete`')

        for i, member in enumerate(members, start=1):
            if i % x == 0:
                percentage_complete += percentage
                await msg.edit(content=f'`{percentage_complete}% Complete`')

            if not member or member.bot or self.eventmember in member.roles:
                continue

            try:
                await member.add_roles(self.eventmember)
            except:
                continue

            await sleep(0.8)
        return await msg.edit(content=f'`100% Complete`')

    @commands.command(aliases=['ии'])
    @commands.has_any_role(MENTOR_ROLE, EVENTER_ROLE)
    @required_args(3)
    async def ee(self, ctx, *args):
        mercstar = get(ctx.guild.emojis, name="avasilver")
        cls = self.find_class(' '.join(args[:2]))

        kwargs = {
            'event_maker': ctx.author.mention,
            'event_date': args[1],
            'event_link': args[2],
            'emojis': {'avasilver': mercstar}
        }

        if not cls:
            cls = self.find_class(args[0])
        else:
            kwargs['event_date'] = args[2]
            kwargs['event_link'] = args[3]

        if not cls:
            return await ctx.send('Не нашел такого ивента')

        try:
            cls_args = list(inspect.signature(cls.__init__).parameters.keys())[1:-1]

            if cls_args:
                for i, arg in enumerate(cls_args, 3):
                    kwargs[arg] = args[i]

            c = cls(**kwargs)
            await ctx.message.delete()
            return await ctx.send(content=self.eventmember.mention, embed=c.embed)
        except:
            return await ctx.send('Что-то не хватает')

    def find_class(self, event_name):
        for m in inspect.getmembers(games, inspect.isclass):
            if m[1].__module__ == 'embeds.games':
                if event_name in m[1].title.lower():
                    return m[1]

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(GUILD_ID)
        self.create_channel_room = self.guild.get_channel(EVENT_START_ROOM_ID)
        self.category = get(self.guild.categories, id=self.create_channel_room.category_id)
        self.eveter = self.guild.get_role(EVENTER_ROLE)
        self.mentor = self.guild.get_role(MENTOR_ROLE)
        self.eventmember = self.guild.get_role(EVENTMEMBER_ROLE)

        self.start_loop.start()

    @tasks.loop(seconds=3)
    async def start_loop(self):
        await self.create_event()
        await self.add_perms()
        self.save_events()

    async def add_perms(self):
        for ch in self.category.voice_channels:
            if ch == self.create_channel_room:
                continue

            try:
                tc_id = self.event_rooms[ch.id]
            except:
                continue

            tc = self.guild.get_channel(tc_id)

            if not tc:
                continue

            for member in ch.members:
                if not member:
                    continue

                overwrite = tc.overwrites_for(member)
                if not overwrite.read_messages:
                    await tc.set_permissions(
                        member, overwrite=PermissionOverwrite(
                            read_messages=True, send_messages=True, attach_files=True,  read_message_history=True,
                        )
                    )

            for member in tc.overwrites:
                if not member or member == self.guild.default_role:
                    continue

                if member == self.mentor or tc.overwrites[member].manage_roles:
                    continue

                if member not in ch.members:
                    await tc.set_permissions(member, overwrite=None)

    async def create_event(self):
        for member in self.create_channel_room.members:
            vc = await self.create_voice_room(member)
            tc = await self.create_text_room(member)

            self.event_rooms[vc.id] = tc.id
            await member.move_to(vc)

    async def create_voice_room(self, member):
        perms = PermissionOverwrite(
            manage_channels=True, move_members=True, manage_nicknames=True, mute_members=True, priority_speaker=True,
            manage_messages=True, administrator=True, stream=True, send_messages=True, read_messages=True,
            manage_webhooks=True, speak=True, manage_roles=True, deafen_members=True
        )
        overwrites = {
            member: perms,
            self.mentor: perms
        }
        vc = await self.category.create_voice_channel(f"Event #{member.discriminator}", overwrites=overwrites)
        return vc

    async def create_text_room(self, member):
        perms = PermissionOverwrite(
            manage_channels=True, manage_messages=True, read_messages=True, send_messages=True, mute_members=True,
            attach_files=True, deafen_members=True, administrator=True, manage_roles=True,
            move_members=True, manage_nicknames=True, priority_speaker=True,
            stream=True, speak=True
        )

        overwrites = {
            self.guild.default_role: PermissionOverwrite(
                read_messages=False, send_messages=False,  read_message_history=True
            ),
            member: perms,
            self.mentor: perms,
        }
        tc = await self.category.create_text_channel(f"Event #{member.discriminator}", overwrites=overwrites)
        return tc

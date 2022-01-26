from asyncio import sleep

from discord.ext import commands, tasks

from systems.money_system import money_system
from base import BaseCog

from config import GUILD_ID


class ActivityCog(BaseCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.members = {}
        self.guild = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(GUILD_ID)
        self.voice_activity.start()

    @commands.Cog.listener()
    async def on_message(self, msg):
        if not msg.content.startswith(self.bot.command_prefix):
            if not self.members.get(msg.author.id):
                self.members[msg.author.id] = 1
            else:
                self.members[msg.author.id] += 1

            if self.members[msg.author.id] == 5:
                del self.members[msg.author.id]
                money_system.add_activity(msg.author.id)

    @tasks.loop()
    async def voice_activity(self):
        members = set()
        after_members = set()

        for ch in self.guild.voice_channels:
            for member in ch.members:
                if member.bot:
                    continue
                members.add(member.id)

        await sleep(300)

        if members:
            for ch in self.guild.voice_channels:
                after_members.update({member.id for member in ch.members})

            members = list(members.intersection(after_members))
            money_system.add_activity_many(members)

from datetime import datetime, timedelta

from pymongo import MongoClient
from discord.ext import commands, tasks

from systems.money_system import money_system
from base import BaseCog

from config import GUILD_ID, ADMIN


class GayNiggerClient(BaseCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.client = MongoClient()
        self._db = self.client.avacord
        self.guild = None

        self.adm_ban_times = self.db.adm_ban_times
        self.mutes = self.db.mutes
        self.warns = self.db.warns
        self.everyday_bonus = self.db.everyday_bonus
        self.personal_roles = self.db.personal_roles
        self.privilegies = self.db.privilegies
        self.server_mutes = self.db.server_mutes
        self.love_rooms = self.db.love_rooms
        self.premium_roles = self.db.premium_roles

        self.mute_role = None
        self.warn_role = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(GUILD_ID)
        self.mute_role = self.guild.get_role(ADMIN['MUTE_ROLE'])
        self.warn_role = self.guild.get_role(ADMIN['WARN_ROLE'])

        self.delete_mutes.start()
        self.delete_everyday_bonus.start()
        self.add_energy.start()

    @property
    def db(self):
        return self._db

    @tasks.loop(minutes=1)
    async def add_energy(self):
        money_system.add_energy_to_all()

    @tasks.loop(seconds=3)
    async def delete_mutes(self):
        for doc in self.server_mutes.find({'unmute_date': {'$lt': datetime.now()}}):
            for vc in self.guild.voice_channels:
                for member in vc.members:
                    if member.id == doc['member_id']:
                        try:
                            await member.edit(mute=False, reason='Серверный мут истек')
                            self.server_mutes.remove({'member_id': member.id})
                        except:
                            continue

        for doc in self.mutes.find({'unmute_date': {'$lt': datetime.now()}}):
            member = self.guild.get_member(doc['member_id'])

            if member:
                await member.remove_roles(self.mute_role, reason="Мут истек")
            self.mutes.remove({'member_id': doc['member_id']})

    @tasks.loop(seconds=3)
    async def delete_everyday_bonus(self):
        docs = self.warns.find({'unwarn_date': {'$lt': datetime.now().replace(microsecond=0)}})

        for doc in docs:
            member = self.guild.get_member(doc['member_id'])

            if member:
                await member.remove_roles(self.warn_role, reason='Варн истек')
            self.warns.remove({'member_id': doc['member_id']})

        now = datetime.now().replace(microsecond=0)

        self.adm_ban_times.update_many(
            {'date_use': {'$lt': now - timedelta(hours=1)}, 'cnt': {'$gt': 0}},
            {'$inc': {'cnt': -1}, '$set': {'date_use': now}}
        )

        docs = self.personal_roles.find({'expiration_date': {'$lt': datetime.now()}}, projection={'_id': False, 'role_id': True})

        for row in docs:
            self.premium_roles.remove({'role_id': row['role_id']})
            await self.guild.get_role(row['role_id']).delete()

        self.personal_roles.remove({'expiration_date': {'$lt': datetime.now()}}, multi=True)
        self.everyday_bonus.remove({'get_date': {'$lt': datetime.now() - timedelta(hours=12)}}, multi=True)

        docs = self.privilegies.find({'expiration_date': {'$lt': datetime.now()}}, projection={'_id': False})

        for row in docs:
            member = self.guild.get_member(row['member_id'])

            if not member:
                continue

            role = self.guild.get_role(row['role_id'])
            await member.remove_roles(role)
            self.privilegies.remove({'member_id': row['member_id']})

        for doc in self.love_rooms.find({'expiration_date': {'$lt': datetime.now()}}):
            vc_id = doc['love_room_id']
            vc = self.guild.get_channel(vc_id)

            if vc:
                await vc.delete(reason='Лаврума истекла')
                self.love_rooms.remove({'love_room_id': vc.id})

from pymongo import DESCENDING

from discord.ext.commands import CommandError

from . import BaseSystem


class _ProfileSystem(BaseSystem):
    fields = {
        'member_id', 'status', 'marriage', 'clan_role_id', 'voice_time', 'love_role_id', 'love_room_id', 'reports_cnt',
        'reputation', 'max_reputation', 'img_url'
    }

    @property
    def collection(self):
        return self.db.profiles

    @property
    def top_reports(self):
        return self.collection.find(
            {'reports_cnt': {'$gte': 1}}, projection={'reports_cnt': True, '_id': False, 'member_id': True}
        ).sort('reports_cnt', DESCENDING).limit(30)

    @property
    def top_voice(self):
        return self.collection.find(
            {'voice_time': {'$gte': 1}}, projection={'voice_time': True, '_id': False, 'member_id': True}
        ).sort('voice_time', DESCENDING).limit(50)

    def delete_clan(self, member_id: int):
        self.collection.update_one({'member_id': member_id}, {'$set': {'clan_role_id': None}})

    def set_love_role_id(self, member_id: int, with_member_id: int, love_role_id: int):
        self.collection.update_many(
            {'member_id': {'$in': [member_id, with_member_id]}}, {'$set': {'love_role_id': love_role_id}}
        )

    def delete_marriage(self, member_id: int):
        self.collection.update_one({'member_id': member_id}, {'$set': {'marriage': None}})

    def delete_love_role(self, member_id: int, with_member_id: int):
        self.collection.update_many({'member_id': {'$in': [member_id, with_member_id]}}, {'$set': {'love_role_id': 0}})

    def delete_clan_roles(self, clan_role_id: int):
        self.collection.update_many({'clan_role_id': clan_role_id}, {'$set': {'clan_role_id': None}})

    def set_img_url(self, member_id: int, url: str):
        self.get_profile(member_id)
        self.collection.update_one({'member_id': member_id}, {'$set': {'img_url': url}})

    def add_voice_time(self, member_id: int, mins: int):
        self.get_profile(member_id)
        self.collection.update_one({'member_id': member_id}, {'$inc': {'voice_time': mins}})

    def set_marriage(self, member_id: int, with_member_id: int):
        self.get_profile(member_id)
        self.collection.update_one({'member_id': member_id}, {'$set': {'marriage': with_member_id}})

    def set_status(self, member_id: int, status: str):
        self.get_profile(member_id)
        self.collection.update_one({'member_id': member_id}, {'$set': {'status': status}})

    def set_clan(self, member_id: int, clan_role_id: int):
        self.get_profile(member_id)
        self.collection.update_one({'member_id': member_id}, {'$set': {'clan_role_id': clan_role_id}})

    def add_reputation(self, member_id: int, points=1):
        res = self.get_profile(member_id)

        if res['max_reputation'] == 1:
            raise CommandError("no money:reputation")

        self.collection.update_one({'member_id': member_id}, {'$inc': {'reputation': points}})

    def del_reputation(self, member_id: int, points=1):
        self.get_profile(member_id)
        self.collection.update_one({'member_id': member_id}, {'$inc': {'reputation': -points}})

    def add_report(self, member_id: int):
        self.get_profile(member_id)
        self.collection.update_one({'member_id': member_id}, {'$inc': {'reports_cnt': 1}})

    def create_profile(self, member_id: int):
        structure = {field: 0 for field in self.fields}
        structure['member_id'] = member_id
        structure['marriage'] = None
        structure['clan_role_id'] = None
        structure['status'] = ' '
        structure['reputation'] = 0
        structure['img_url'] = None

        self.collection.insert_one(structure)
        return structure

    def get_profile(self, member_id: int):
        res = self.collection.find_one({'member_id': member_id})
        return res if res else self.create_profile(member_id)


profile_system = _ProfileSystem()

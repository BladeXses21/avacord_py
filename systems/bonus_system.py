from datetime import datetime

from . import BaseSystem


class _BonusSystem(BaseSystem):

    @property
    def collection(self):
        return self.db.everyday_bonus

    @property
    def privilegies(self):
        return self.db.privilegies

    @property
    def love_rooms(self):
        return self.db.love_rooms

    @property
    def premium_roles(self):
        return self.db.premium_roles

    def add_role(self, member_id: int, role_id: int):
        self.premium_roles.insert_one({
            'member_id': member_id,
            'role_id': role_id,
            'max_slots': 3,
            'slots': 0
        })

    def add_slot(self, member_id: int, role_id: int):
        self.premium_roles.update_one({'member_id': member_id, 'role_id': role_id}, {'$inc': {'slots': -1}})

    def del_slot(self, member_id: int, role_id: int):
        self.premium_roles.update_one({'member_id': member_id, 'role_id': role_id}, {'$inc': {'slots': 1}})

    def get_role(self, member_id: int, role_id: int):
        return self.premium_roles.find_one({"member_id": member_id, 'role_id': role_id})

    def has_privilegies(self, member_id: int, bonus_type: str):
        return self.privilegies.find_one({'member_id': member_id, 'bonus_type': bonus_type})

    def get_love_room(self, member_id: int):
        return self.love_rooms.find_one({'member_id': member_id})

    def inc_love_room(self, member_id: int, dt: datetime):
        self.love_rooms.update_one({'member_id': member_id}, {'$set': {'expiration_date': dt}})

    def inc_privilegies(self, member_id: int, bonus_type: str, dt: datetime):
        self.privilegies.update_one(
            {'member_id': member_id, 'bonus_type': bonus_type}, {'$set': {'expiration_date': dt}}
        )

    def get_privilegies_date(self, member_id: int, bonus_type: str):
        return self.privilegies.find_one({
            'member_id': member_id, 'bonus_type': bonus_type
        }).get('expiration_date', None)

    def buy_love_room(self, member_id: int, love_room_id: int, exp_date: datetime):
        self.love_rooms.insert_one({
            'member_id': member_id,
            'love_room_id': love_room_id,
            'expiration_date': exp_date
        })

    def buy_privilegies(self, member_id: int, role_id: int, exp_date: datetime, bonus_type: str) -> bool:
        self.privilegies.insert_one({
            'member_id': member_id,
            'role_id': role_id,
            'expiration_date': exp_date,
            'bonus_type': bonus_type
        })
        return True

    def has_bonus(self, member_id: int, bonus_type: str) -> bool:
        res = self.collection.find_one({'member_id': member_id, 'bonus_type': bonus_type})

        if res:
            return False
        return True

    def bonus_date(self, member_id: int, bonus_type: str) -> datetime:
        return self.collection.find_one({'member_id': member_id, 'bonus_type': bonus_type}).get('get_date', None)

    def get_bonus(self, member_id: int, bonus_type: str):
        self.collection.insert_one({
            'member_id': member_id,
            'get_date': datetime.now().replace(microsecond=0),
            'bonus_type': bonus_type
        })

    def delete_row(self, member_id: int):
        self.privilegies.delete_one({'member_id': member_id})

    def del_love_room(self, **kwargs):
        self.love_rooms.update_one(kwargs, {'$set': {'expiration_date': datetime.now()}})


bonus_system = _BonusSystem()

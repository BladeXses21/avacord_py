from pymongo import DESCENDING

from errors import NotEnoughCP
from . import BaseSystem


class _ClanSystem(BaseSystem):

    @property
    def collection(self):
        return self.db.clans

    @property
    def clan_requests(self):
        return self.db.clan_requests

    @property
    def pay_cp(self):
        return self.db.pay_cp

    @property
    def top_cw(self):
        return self.collection.find({'cw_points': {'$gte': 1}}).sort('cw_points', DESCENDING).limit(20)

    def add_cw(self, clan_role_id: int, points: int):
        self.collection.update_one({'clan_role_id': clan_role_id}, {'$inc': {'cw_points': points}})

    def add_avatar(self, leader_id: int, avatar_url: str):
        self.collection.update_one({'leader_id': leader_id}, {'$set': {'avatar_url': avatar_url}})

    def get_pay(self, leader_id=None, clan_role_id=None):
        res = None

        if leader_id:
            res = self.pay_cp.find_one({'leader_id': leader_id})['cost']
        elif clan_role_id:
            res = self.pay_cp.find_one({'clan_role_id': clan_role_id})['cost']

        if not res:
            return False
        return res

    def add_pay(self, leader_id: int, clan_role_id: int, cost: int) -> bool:
        if self.pay_cp.find_one({'leader_id': leader_id}):
            return False

        self.pay_cp.insert_one({'leader_id': leader_id, 'clan_role_id': clan_role_id, 'cost': cost})
        return True

    def delete_pay(self, leader_id: int):
        self.pay_cp.delete_one({'leader_id': leader_id})

    def get_clans(self, page, limit):
        return self.collection.find({}, projection={'_id': False}).sort(
            'clan_points', DESCENDING
        ).limit(limit).skip(page*limit)

    def get_request(self, request_id: int):
        return self.clan_requests.find_one({'request_id': request_id}, projection={'_id': False})

    def has_request(self, leader_id: int, request_id: int) -> bool:
        if self.clan_requests.find_one({'leader_id': leader_id, 'request_id': request_id}):
            return True
        return False

    def delete_request(self, member_id: int) -> bool:
        if not self.clan_requests.find_one({'member_id': member_id}):
            return False

        self.clan_requests.delete_one({'member_id': member_id})
        return True

    def create_request(self, member_id: int, leader_id: int, request_id: int) -> bool:
        if self.clan_requests.find_one({'member_id': member_id, 'leader_id': leader_id}):
            return False

        self.clan_requests.delete_one({'member_id': member_id})
        self.clan_requests.insert_one({'member_id': member_id, 'leader_id': leader_id, 'request_id': request_id})
        return True

    def is_clan_leader(self, leader_id: int) -> bool:
        if self.collection.find_one({'leader_id': leader_id}):
            return True
        return False

    def change_leader(self, leader_id: int, to_leader_id: int):
        self.pay_cp.update_one({'leader_id': leader_id}, {'$set': {'leader_id': to_leader_id}})
        self.collection.update_one({'leader_id': leader_id}, {'$set': {'leader_id': to_leader_id}})

    def get_clan_info_by_role(self, role_id: int):
        return self.collection.find_one({'clan_role_id': role_id}, projection={'_id': False})

    def get_clan_info(self, leader_id: int):
        return self.collection.find_one({'leader_id': leader_id}, projection={'_id': False})

    def change_clan_name(self, leader_id: int, clan_name: str) -> bool:
        if not self.collection.find_one({'leader_id': leader_id}):
            return False

        self.collection.update_one({'leader_id': leader_id}, {'$set': {'clan_name': clan_name}})
        return True

    def add_description(self, leader_id: int, description: str):
        return self.collection.update_one({'leader_id': leader_id}, {'$set': {'description': description}})

    @property
    def clans_roles(self):
        return self.collection.find({}, projection={'clan_role_id': True, '_id': False})

    def add_tc(self, leader_id: int, tc_id: int) -> bool:
        return self.collection.update_one({'leader_id': leader_id}, {'$set': {'tc': tc_id}}).modified_count == 1

    def add_clan_points(self, clan_name: str, points: int) -> bool:
        if not self.collection.find_one({'clan_name': clan_name}):
            return False

        res = self.collection.update_one({'clan_name': clan_name}, {'$inc': {'clan_points': points}})
        return res.modified_count == 1

    def remove_clan_points(self, clan_name: str, points: int) -> bool:
        res = self.collection.find_one({'clan_name': clan_name})

        if not res:
            return False
        elif res['clan_points'] - points < 0:
            raise NotEnoughCP('Недостаточно клан очков')

        res = self.collection.update_one({'clan_name': clan_name}, {'$inc': {'clan_points': -points}})
        return res.modified_count == 1

    def add_clan(self, leader_id: int, clan_name: str, clan_role_id: int, vc: int) -> bool:
        if self.collection.find_one({'leader_id': leader_id}):
            return False

        self.collection.insert_one({
            'leader_id': leader_id,
            'clan_name': clan_name,
            'clan_role_id': clan_role_id,
            'clan_points': 0,
            'vc': vc,
            'tc': 0,
            'description': None,
            'avatar_url': None,
            'cw_points': 0
        })
        return True

    def delete_clan(self, leader_id: int) -> tuple:
        res = self.collection.find_one({'leader_id': leader_id})

        if not res:
            return ()

        self.collection.delete_one({'leader_id': leader_id})
        return res['clan_role_id'], res['vc'], res['tc']


clan_system = _ClanSystem()

from datetime import datetime

from pymongo import DESCENDING
from discord.ext.commands import CommandError

from . import BaseSystem

from config import START_MONEY


class _MoneySystem(BaseSystem):
    fields = {
        'member_id', 'gold', 'silver', 'energy', 'pvp', 'activity'
    }

    @property
    def tmp_money(self):
        return self.db.tmp_money

    @property
    def collection(self):
        return self.db.money

    @property
    def top_currency(self):
        return self.collection.find(
            {'silver': {'$gte': 1}}, projection={'member_id': True, 'silver': True, '_id': False}
        ).sort('silver', DESCENDING).limit(15)

    @property
    def top_donate(self):
        return self.collection.find(
            {'gold': {'$gte': 1}}, projection={'gold': True, '_id': False, 'member_id': True}
        ).sort('gold', DESCENDING).limit(50)

    @property
    def top_activity(self):
        return self.collection.find(
            {'activity': {'$gte': 1}}, projection={'activity': True, '_id': False, 'member_id': True}
        ).sort('activity', DESCENDING).limit(50)

    def del_activty(self):
        self.collection.update_many({}, {'$set': {'activity': 0}})

    def add_activity(self, member_id: int, points=1):
        self.get_wallet(member_id)
        self.collection.update_one({'member_id': member_id}, {'$inc': {'activity': points}})

    def add_activity_many(self, member_ids: list, points=1):
        for member_id in member_ids:
            self.get_wallet(member_id)

        self.collection.update_many({'member_id': {'$in': member_ids}}, {'$inc': {'activity': points}})

    def add_energy_to_all(self):
        self.collection.update_many({'energy': {'$lte': 99}}, {'$inc': {'energy': 1}})

    def get_wallet(self, member_id: int):
        res = self.collection.find_one({'member_id': member_id})
        return res if res else self.create_purse(member_id)

    def add_money(self, member_id: int, currency: dict):
        assert {*currency}.intersection(self.fields) != set(), 'No fields found'
        self.get_wallet(member_id)

        for k, v in currency.items():
            currency[k] = abs(v)

        self.collection.update_one({'member_id': member_id}, {'$inc': currency})

    def take_money(self, member_id: int, currency: dict):
        assert {*currency.keys()}.intersection(self.fields) != set(), 'No fields found'
        res = self.get_wallet(member_id)

        for k in currency:
            money = abs(currency[k])

            if res[k] - money < 0:
                raise CommandError(f'no money:{k}')

            currency[k] = -money

        if currency.get('silver'):
            self.add_activity(member_id, int(abs(currency['silver'])*30/100))
        if currency.get('gold'):
            self.add_activity(member_id, int(abs(currency['gold'])))

        self.collection.update_one({'member_id': member_id}, {'$inc': currency})

    def take_to_zero(self, member_id: int, currency: dict):
        assert {*currency}.intersection(self.fields) != set(), 'No fields found'
        res = self.get_wallet(member_id)

        for k in currency:
            money = abs(currency[k])
            diff = res[k] - money

            if diff < 0:
                diff = 0

            currency[k] = diff

        self.collection.update_one({'member_id': member_id}, {'$set': currency})

    def create_purse(self, member_id: int) -> dict:
        structure = {field: 0 for field in self.fields}
        structure['member_id'] = member_id
        structure.update(START_MONEY)

        self.collection.insert_one(structure)
        return structure

    def deposit(self, member_id: int, currency: dict) -> bool:
        self.take_money(member_id, currency.copy())

        res = self.tmp_money.find_one({'member_id': member_id})

        if not res:
            self.create_tmp(member_id)

        currency.update({'transaction_date': datetime.now().replace(microsecond=0)})
        self.tmp_money.update_one({'member_id': member_id}, {'$set': currency})
        return True

    def cash_out(self, member_id: int) -> bool:
        if not self._transact_money(member_id):
            return False
        return True

    def transact_money(self, member_id: int, to_member_id: int, currency: dict) -> bool:
        if not self.take_money(member_id, currency.copy()):
            return False

        self.add_money(to_member_id, currency)
        return True

    def _transact_money(self, member_id: int, to_member_id=None) -> bool:
        res = self.tmp_money.find_one(
            {'member_id': member_id},
            {'transaction_date': False, 'member_id': False, '_id': False}
        )

        if not res:
            return False

        self.add_money(to_member_id if to_member_id else member_id, res)
        self.delete_tmp(member_id)
        return True

    def give_money(self, member_id: int, to_member_id: int) -> bool:
        if not self._transact_money(member_id, to_member_id):
            return False
        return True

    def create_tmp(self, member_id: int):
        self.tmp_money.insert_one({
            'member_id': member_id,
            'stars': 0
        })

    def delete_tmp(self, member_id: int):
        self.tmp_money.delete_one({'member_id': member_id})


money_system = _MoneySystem()

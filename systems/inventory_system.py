from datetime import datetime, timedelta

from discord.ext.commands import CommandError

from . import BaseSystem


class _InventorySysten(BaseSystem):
    fields = {
        'member_id', 'role_2', 'role_3', 'role_6', 'rings', 'drings', 'rring', 'bgift', 'sgift', 'batteries', 'pillows',
        'cakes'
    }

    @property
    def collection(self):
        return self.db.inventories

    @property
    def personal_roles(self):
        return self.db.personal_roles

    def del_role(self, role_id: int):
        self.personal_roles.update_one({'role_id': role_id}, {'$set': {'expiration_date': datetime.now()}})

    def get_inventory(self, member_id: int):
        res = self.collection.find_one({'member_id': member_id})
        return res if res else self.create_inventory(member_id)

    def add_personal_role(self, role_id: int, days: int):
        now = datetime.now().replace(microsecond=0) + timedelta(days=days)
        self.personal_roles.insert_one({
            'role_id': role_id,
            'expiration_date': now
        })

    def create_inventory(self, member_id: int) -> dict:
        structure = {field: 0 for field in self.fields}
        structure['member_id'] = member_id
        self.collection.insert_one(structure)
        return structure

    def take_item(self, member_id: int, item: dict):
        res = self.get_inventory(member_id)

        for k in item:
            money = abs(item[k])

            if res[k] - money < 0:
                raise CommandError(f'no money:{k}')

            item[k] = -money

        self.collection.update_one({'member_id': member_id}, {'$inc': item})

    def add_item(self, member_id: int, item: dict):
        self.get_inventory(member_id)

        for k, v in item.items():
            item[k] = abs(v)

        self.collection.update_one({'member_id': member_id}, {'$inc': item})


inventory_system = _InventorySysten()

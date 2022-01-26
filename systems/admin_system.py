from datetime import datetime, timedelta

from . import BaseSystem


class _AdminSystem(BaseSystem):

    @property
    def reports(self):
        return self.db.reports

    def create_report(self, member_id: int, from_id: int, reason: str, request_id: int, created_date: datetime, msg_id):
        self.reports.insert_one({
            'from_id': from_id,
            'member_id': member_id,
            'reason': reason,
            'request_id': request_id,
            'date': created_date,
            'msg_id': msg_id
        })

    def get_report(self, request_id: int):
        return self.reports.find_one({'request_id': request_id})

    def delete_report(self, request_id: int) -> bool:
        return self.reports.delete_one({'request_id': request_id}).deleted_count == 1

    @property
    def collection(self):
        return self.db.admin_bans

    def add_ban(self, member_id: int, admin_id: int, reason: str):
        self.collection.insert_one({
            'member_id': member_id,
            'who_id': admin_id,
            'reason': reason,
            'ban_date': datetime.now().replace(microsecond=0)
        })

    @property
    def ban_times(self):
        return self.db.adm_ban_times

    def add_ban_time(self, admin_id: int) -> bool:
        res = self.ban_times.find_one({'member_id': admin_id})

        if not res:
            self.ban_times.insert_one({
                'member_id': admin_id,
                'cnt': 1,
                'date_use': datetime.now().replace(microsecond=0)
            })
            return True
        elif res['cnt'] == 5:
            return False

        self.ban_times.update_one(
            {'member_id': admin_id}, {'$inc': {'cnt': 1}, '$set': {'date_use': datetime.now().replace(microsecond=0)}}
        )
        return True

    def remove_ban_time(self, admin_id: int):
        self.ban_times.update_one(
            {'member_id': admin_id}, {'$inc': {'cnt': -1}, '$set': {'date_use': datetime.now().replace(microsecond=0)}}
        )

    @property
    def mutes(self):
        return self.db.mutes

    @property
    def server_mutes(self):
        return self.db.server_mutes

    def has_mute(self, member_id: int) -> bool:
        return True if self.mutes.find_one({'member_id': member_id}) else False

    def has_server_mute(self, member_id: int) -> bool:
        return True if self.server_mutes.find_one({'member_id': member_id}) else False

    def add_mute(self, member_id: int, moder_id: int, reason: str, unmute_date: datetime):
        structure = {
            'member_id': member_id,
            'who_id': moder_id,
            'reason': reason,
            'mute_date': datetime.now().replace(microsecond=0),
            'unmute_date': unmute_date
        }
        self.mutes.insert_one(structure)

    def add_server_mute(self, member_id: int, moder_id: int, reason: str, unmute_date: datetime):
        structure = {
            'member_id': member_id,
            'who_id': moder_id,
            'reason': reason,
            'mute_date': datetime.now().replace(microsecond=0),
            'unmute_date': unmute_date
        }
        self.server_mutes.insert_one(structure)

    def delete_server_mute(self, member_id: int):
        self.server_mutes.delete_one({'member_id': member_id})

    def change_mute_date(self, member_id: int):
        self.mutes.update_one(
            {'member_id': member_id}, {'$set': {'unmute_date': datetime.now() - timedelta(days=1)}}
        )

    def delete_mute(self, member_id: int):
        self.mutes.delete_one({'member_id': member_id})

    @property
    def warns(self):
        return self.db.warns

    def create_warn(self, member_id: int, moder_id: int, reason: str) -> bool:
        res = self.warns.find_one({'member_id': member_id})

        if res:
            return False

        now = datetime.now().replace(microsecond=0)

        self.warns.insert_one({
            'member_id': member_id,
            'who_id': moder_id,
            'reason': reason,
            'warn_date': now,
            'unwarn_date': now + timedelta(hours=24)
        })
        return True

    def remove_all(self):
        self.warns.delete_many({})

    def delete_warn(self, member_id: int) -> bool:
        return self.warns.delete_one({'member_id': member_id}).deleted_count == 1


admin_system = _AdminSystem()

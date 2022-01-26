from . import BaseSystem


class _VoiceSystem(BaseSystem):

    @property
    def collection(self):
        return self.db.voice_time

    def add_mins(self, members_ids: list):
        self.collection.update_many(
            {'member_id': {'$in': members_ids}},
            {'$inc': {'mins': 1}},
        )

    def delete_mins(self, member_id: int):
        self.collection.update_one({'member_id': member_id}, {'$set': {'mins': 0}})

    def add_members(self, member_ids: list):
        self.collection.insert_many([{'member_id': member_id} for member_id in member_ids])

    def get_members_from_list(self, members_ids: list):
        return self.collection.find({'member_id': {'$in': members_ids}}, projection={'_id': False, 'member_id': True})

    def get_minutes(self, member_id: int):
        res = self.collection.find_one({'member_id': member_id})

        if not res:
            res = {'member_id': member_id, 'mins': 0}
            self.collection.insert_one(res)

        return res


# voice_system = _VoiceSystem()

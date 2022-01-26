from . import BaseSystem


class _EventsSystem(BaseSystem):

    @property
    def collection(self):
        return self.db.events_awards

    def add_row(self, eventer_id: int, member_id: int, cost: int, event_name: str, request_id: int, msg_id: int, dt):
        self.collection.insert_one({
            'eventer_id': eventer_id,
            'member_id': member_id,
            'cost': cost,
            'event_name': event_name,
            'request_id': request_id,
            'msg_id': msg_id,
            'creation_date': dt
        })

    def get_event(self, eventer_id=None, member_id=None, cost=None, event_name=None, request_id=None, msg_id=None):
        if eventer_id:
            return self.collection.find_one({'eventer_id': eventer_id})
        elif member_id:
            return self.collection.find_one({'member_id': member_id})
        elif cost:
            return self.collection.find_one({'member_id': member_id})
        elif event_name:
            return self.collection.find_one({'event_name': event_name})
        elif request_id:
            return self.collection.find_one({'request_id': request_id})
        elif msg_id:
            return self.collection.find_one({'msg_id': msg_id})
        raise AssertionError()

    def delete_event(self, request_id: int):
        return self.collection.delete_one({'request_id': request_id}).deleted_count == 1


events_system = _EventsSystem()

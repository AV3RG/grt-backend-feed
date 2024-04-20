import random

from sqlalchemy import insert

from WebGLTable import WebGLTable
from db import async_session
from push_data import PushData


class Cache:
    def __init__(self):
        self.cache = dict()
        self.queued_data = []
        self.busy_state = False

    def add(self, value: PushData):
        key_range_max = 1000000000000000000000
        key = random.randint(0, key_range_max)
        while key in self.cache:
            key = random.randint(0, key_range_max)

        self.cache[key] = {
            "data": value,
            "queued": False
        }

    def get_cache_dict(self):
        return self.cache

    async def update_and_cleanup(self):
        if self.busy_state:
            return
        self.busy_state = True
        self.queue_all()
        if len(self.queued_data) == 0:
            self.busy_state = False
            return
        success = await self.update_on_db()
        if success:
            self.cleanup()
        else:
            self.mark_all_as_unqueued()
        self.busy_state = False

    def queue_all(self):
        for key in self.cache:
            if not self.cache[key]["queued"]:
                self.cache[key]["queued"] = True
                self.queued_data.append(self.cache[key]["data"])
        return True

    async def update_on_db(self):
        async with async_session() as session:
            to_send = []
            for data in self.queued_data:
                entry = data.dict()
                to_send.append(entry)
            statement = insert(WebGLTable).values(to_send)
            try:
                await session.execute(statement)
                await session.commit()
                return True
            except Exception as e:
                print(e)
                return False

    def cleanup(self):
        print("Cleaning up")
        keys_to_delete = []
        for key in self.cache:
            if self.cache[key]["queued"]:
                keys_to_delete.append(key)
        print(f"Keys to delete: {keys_to_delete}")
        for key in keys_to_delete:
            del self.cache[key]

        self.queued_data = []
        return True

    def mark_all_as_unqueued(self):
        for key in self.cache:
            self.cache[key]["queued"] = False
        return True

import os
import time
from datetime import datetime, timedelta
from typing import Optional

from dotenv import load_dotenv
from FtApi import FtApi
from FtApi.FtApi import HttpMethod


class FtApiClient:
    SLEEP_TIME = timedelta(seconds=0.6)

    def __init__(self) -> None:
        load_dotenv()
        uid = os.getenv("FT_CLIENT_UID")
        secret = os.getenv("FT_CLIENT_SECRET")
        self.ft_api = FtApi(uid, secret)
        self.last_request_time: Optional[datetime] = None

    def sleep(self) -> None:
        now = datetime.now()
        if not self.last_request_time:
            self.last_request_time = now
            return
        delta = now - self.last_request_time
        if delta < self.SLEEP_TIME:
            time.sleep((self.SLEEP_TIME - delta).microseconds / 1000000)
        self.last_request_time = now

    def get_scale_teams(self, kwargs: dict) -> list:
        request = self.ft_api.Scale_teams(**kwargs)
        return self._get_resources(request)

    def get_user_scale_teams(self, user_id, kwargs: dict) -> list:
        request = self.ft_api.UsersScale_teams(user_id, **kwargs)
        return self._get_resources(request)

    def get_campus(self, kwargs: dict) -> list:
        request = self.ft_api.Campus(**kwargs)
        return self._get_resources(request)

    def get_cursus_users(self, kwargs: dict) -> list:
        request = self.ft_api.Cursus_users(**kwargs)
        return self._get_resources(request)

    def get_events(self, campus_id: int, cursus_id: int, kwargs: dict) -> list:
        request = self.ft_api.CampusCursusEvents(campus_id, cursus_id, **kwargs)
        return self._get_resources(request)

    def _get_resources(self, request: HttpMethod) -> list:
        resources = []
        while True:
            self.sleep()
            resource = request.Get()
            resources += resource
            if len(resource) != request.page["size"]:
                break
            print(f"{len(resources)} items")
        return resources

import os
import time
from datetime import datetime, timedelta
from typing import Optional

from dotenv import load_dotenv
from FtApi import FtApi


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
        scale_teams_list = []
        while True:
            self.sleep()
            scale_teams = request.Get()
            scale_teams_list += scale_teams
            if len(scale_teams) != request.page["size"]:
                break
            print(f"{len(scale_teams_list)} items")
        return scale_teams_list

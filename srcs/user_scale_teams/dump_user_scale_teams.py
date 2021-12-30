import json
from datetime import datetime
from typing import List

from api import FtApiClient


def dump_scale_teams(login: str, campus_id: List[int], cursus_id: List[int]) -> None:
    client = FtApiClient()
    kwargs = {
        "range": {},
        "sort": "-created_at",
        "filter": {},
    }

    print(f"login: {login}")
    if campus_id:
        kwargs["filter"]["campus_id"] = ",".join(map(str, campus_id))
        print(f"campus_id: {kwargs['filter']['campus_id']}")
    if cursus_id:
        kwargs["filter"]["cursus_id"] = ",".join(map(str, cursus_id))
        print(f"cursus_id: {kwargs['filter']['cursus_id']}")

    scale_teams = client.get_user_scale_teams(login, kwargs)

    now_time = datetime.now().strftime("%Y%m%d-%H%M")
    json_file_path = f"user_scale_teams_{login}_{now_time}.json"
    with open(json_file_path, "w") as f:
        json.dump(scale_teams, f)

    print(f"Dumped user_scale_teams: {json_file_path}")

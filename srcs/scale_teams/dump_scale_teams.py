import json
from datetime import datetime
from typing import List

from api import FtApiClient

# TODO: parametrize created_at
RANGE_CREATED_AT = "2021-01-01T09:00:00.000Z,2022-01-01T08:59:59.999Z"
JSON_FILE_PATH = f"scale_teams_{datetime.now().strftime('%Y%m%d-%H%M')}.json"


def dump_scale_teams(campus_id: List[int], cursus_id: List[int]) -> None:
    client = FtApiClient()
    kwargs = {
        "range": {"created_at": RANGE_CREATED_AT},
        "sort": "-created_at",
        "filter": {},
    }
    if campus_id:
        kwargs["filter"]["campus_id"] = ",".join(map(str, campus_id))
        print(f"campus_id: {kwargs['filter']['campus_id']}")
    if cursus_id:
        kwargs["filter"]["cursus_id"] = ",".join(map(str, cursus_id))
        print(f"cursus_id: {kwargs['filter']['cursus_id']}")
    scale_teams = client.get_scale_teams(kwargs)
    with open(JSON_FILE_PATH, "w") as f:
        json.dump(scale_teams, f)

    print(f"Dumped scale_teams: {JSON_FILE_PATH}")

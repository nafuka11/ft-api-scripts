import json
from datetime import datetime
from typing import List, Optional

from api import FtApiClient

JSON_FILE_PATH = f"scale_teams_{datetime.now().strftime('%Y%m%d-%H%M')}.json"


def dump_scale_teams(
    campus_id: Optional[List[int]],
    cursus_id: Optional[List[int]],
    begin_at: Optional[List[str]],
) -> None:
    client = FtApiClient()
    kwargs = {
        "range": {},
        "sort": "-begin_at",
        "filter": {},
    }
    if campus_id:
        kwargs["filter"]["campus_id"] = ",".join(map(str, campus_id))
        print(f"campus_id: {kwargs['filter']['campus_id']}")
    if cursus_id:
        kwargs["filter"]["cursus_id"] = ",".join(map(str, cursus_id))
        print(f"cursus_id: {kwargs['filter']['cursus_id']}")
    if begin_at:
        kwargs["range"]["begin_at"] = ",".join(begin_at)
        print(f"begin_at: {kwargs['range']['begin_at']}")
    scale_teams = client.get_scale_teams(kwargs)
    with open(JSON_FILE_PATH, "w") as f:
        json.dump(scale_teams, f)

    print(f"Dumped scale_teams: {JSON_FILE_PATH}")

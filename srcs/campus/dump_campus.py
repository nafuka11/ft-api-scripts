from typing import List, Optional

from api import FtApiClient
from utils.file_io import save_json

CAMPUS_JSON = "campus.json"


def dump_campus_and_cursus_users(
    cursus_id: Optional[List[int]], begin_at: Optional[List[str]]
) -> None:
    client = FtApiClient()
    kwargs = {
        "sort": "id",
    }
    campuses = client.get_campus(kwargs)

    dump_campuses(campuses)

    if cursus_id:
        cursus_ids = ",".join(map(str, cursus_id))
        print(f"cursus_id: {cursus_ids}")
    if begin_at:
        begin_at_str = f"{begin_at[0]},{begin_at[1]}"
        print(f"begin_at: {begin_at_str}")

    for campus in campuses:
        dump_cursus_users(client, cursus_id, begin_at, campus)


def dump_campuses(campuses: list) -> None:
    save_json(CAMPUS_JSON, campuses)


def dump_cursus_users(
    client: FtApiClient,
    cursus_id: Optional[List[int]],
    begin_at: Optional[List[str]],
    campus: list,
) -> None:
    kwargs = {
        "range": {},
        "filter": {
            "campus_id": campus["id"],
        },
    }
    if cursus_id:
        kwargs["filter"]["cursus_id"] = ",".join(map(str, cursus_id))
    if begin_at:
        kwargs["range"]["begin_at"] = f"{begin_at[0]},{begin_at[1]}"

    print(f"Fetch cursus_users: campus id={campus['id']} name={campus['name']}")
    cursus_users = client.get_cursus_users(kwargs)

    json_file_path = generate_json_file_path(cursus_id, campus["id"])
    save_json(json_file_path, cursus_users)


def generate_json_file_path(cursus_id: Optional[List[int]], campus_id: int) -> str:
    cursus_id_str = ""
    if cursus_id:
        cursus_id_str = f"cursusid_{'_'.join(map(str, cursus_id))}_"
    json_file_path = f"cursus_users_{cursus_id_str}campusid_{campus_id}.json"
    return json_file_path

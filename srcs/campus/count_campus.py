import json
import re
from datetime import datetime
from io import TextIOWrapper
from typing import List, Optional

from utils.file_io import save_csv

DATE_INF = datetime(4242, 12, 31, 23, 59, 59)
CAMPUS_BLACKHOLED_CSV = "campus_blackholed.csv"


def count_cursus_users(
    campus_file: TextIOWrapper, cursus_user_files: List[TextIOWrapper]
) -> None:
    campuses = load_campus_file(campus_file)
    rows = []
    for file in cursus_user_files:
        rows.append(count_file(file, campuses))
    write_csv(rows)


def load_campus_file(file: TextIOWrapper) -> list:
    campuses = json.load(file)
    file.close()
    return campuses


def count_file(file: TextIOWrapper, campuses: list) -> list:
    now_time = datetime.utcnow()
    cursus_users = json.load(file)
    campus_id = int(
        re.sub(
            r".*cursus_users_(cursusid_[\d,_]+)campusid_(\d+).*\.json", r"\2", file.name
        )
    )
    file.close()

    active_user = 0
    blackholed_user = 0
    for user in cursus_users:
        if not user["begin_at"]:
            continue

        begin_at = convert_iso_to_date(user["begin_at"])
        if user["blackholed_at"]:
            blackholed_at = convert_iso_to_date(user["blackholed_at"])
        else:
            blackholed_at = DATE_INF
        if user["end_at"]:
            end_at = convert_iso_to_date(user["end_at"])
        else:
            end_at = DATE_INF

        if now_time < begin_at:
            continue
        if now_time > blackholed_at or now_time > end_at:
            blackholed_user += 1
        else:
            active_user += 1

    total_user = active_user + blackholed_user
    percent = 0
    if total_user != 0:
        percent = blackholed_user / total_user

    campus_name = find_campus_name(campus_id, campuses)

    return [campus_name, active_user, blackholed_user, total_user, percent]


def write_csv(rows: list) -> None:
    header = ["campus", "active_user", "blackholed_user", "total_user", "percent"]
    rows.insert(0, header)
    save_csv(CAMPUS_BLACKHOLED_CSV, rows)


def find_campus_name(campus_id: int, campuses: list) -> Optional[str]:
    for campus in campuses:
        if campus["id"] == campus_id:
            return campus["name"]
    return None


def convert_iso_to_date(date_str: str) -> datetime:
    time = datetime.fromisoformat(date_str.replace("Z", ""))
    return time

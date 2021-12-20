import csv
import json
from collections import Counter
from io import TextIOWrapper
from typing import Any, List

SCALE_TEAMS_CSV_PATH = "scale_teams.csv"
CORRECTORS_CSV_PATH = "correctors.csv"


def count_scale_teams(json_file: TextIOWrapper) -> None:
    scale_teams = read_json(json_file)
    count_and_save_file(scale_teams)


def read_json(json_file: TextIOWrapper) -> Any:
    objects = json.load(json_file)
    json_file.close()
    return objects


def count_and_save_file(scale_teams: list) -> None:
    scale_team_rows = []
    correctors: List[str] = []
    for team in scale_teams:
        correctors.append(team["corrector"]["login"])
        scale_team_rows.append(
            [
                team["id"],
                team["scale_id"],
                team["team"]["project_id"],
                team["created_at"],
                team["corrector"]["login"],
                " ".join([corrected["login"] for corrected in team["correcteds"]]),
            ]
        )

    counter = Counter(correctors)
    corrector_rows = counter.most_common()

    with open(SCALE_TEAMS_CSV_PATH, "w") as f:
        writer = csv.writer(f)
        writer.writerows(scale_team_rows)

    with open(CORRECTORS_CSV_PATH, "w") as f:
        writer = csv.writer(f)
        writer.writerows(corrector_rows)

    print(f"Saved reviewers and number of reviews to : {CORRECTORS_CSV_PATH}")
    print(f"Saved scale_teams to : {SCALE_TEAMS_CSV_PATH}")

from argparse import ArgumentParser, Namespace
from typing import Optional

from api import FtApiClient
from utils.file_io import save_csv


def main() -> None:
    args = parse_args()
    dump_event_csv(args.campus_id, args.cursus_id, args.name)


def parse_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument("campus_id", type=int)
    parser.add_argument("cursus_id", type=int)
    parser.add_argument("--name", type=str)
    args = parser.parse_args()

    return args


def dump_event_csv(campus_id: int, cursus_id: int, name: Optional[str] = None) -> None:
    client = FtApiClient()
    kwargs = {"sort": "begin_at"}
    events = client.get_events(campus_id, cursus_id, kwargs)

    if name:
        events = [event for event in events if name in event["name"]]
    attributes = ["id", "name", "begin_at", "nbr_subscribers"]
    rows = [attributes]
    for event in events:
        rows.append([event[attribute] for attribute in attributes])
    filepath = generate_file_path(campus_id, cursus_id, name)
    save_csv(filepath, rows)


def generate_file_path(
    campus_id: int, cursus_id: int, name: Optional[str] = None
) -> str:
    filepath = f"events_{campus_id}_{cursus_id}"
    if name:
        filepath += f"_{name}"

    return f"{filepath}.csv"


if __name__ == "__main__":
    main()

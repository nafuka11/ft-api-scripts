import json
from collections import Counter
from io import TextIOWrapper
from typing import Any, Tuple

from rich import box
from rich.console import Console
from rich.table import Table


def count_scale_teams(login: str, json_file: TextIOWrapper) -> None:
    scale_teams = read_json(json_file)
    reviewer_flags, reviewee_flags = count_flag(login, scale_teams)
    reviewer_table = generate_flags_table(
        reviewer_flags, "Reviewer flags", reviewee_flags
    )
    reviewee_table = generate_flags_table(
        reviewee_flags, "Reviewee flags", reviewer_flags
    )
    show_tables(login, reviewer_table, reviewee_table)


def read_json(json_file: TextIOWrapper) -> Any:
    objects = json.load(json_file)
    json_file.close()
    return objects


def count_flag(login: str, scale_teams: list) -> Tuple[list, list]:
    reviewer_flags = []
    reviewee_flags = []
    for team in scale_teams:
        is_reviewer = team["corrector"]["login"] == login
        is_reviewee = any(
            [corrected["login"] == login for corrected in team["correcteds"]]
        )

        if is_reviewer:
            reviewer_flags.append(team["flag"]["name"])
        elif is_reviewee:
            reviewee_flags.append(team["flag"]["name"])

    return reviewer_flags, reviewee_flags


def generate_flags_table(flags: list, description: str, other_flags: list) -> Table:
    table = Table(
        title=description,
        title_style="bold",
        show_header=True,
        show_footer=True,
        show_edge=False,
        box=box.SIMPLE,
        header_style="bold cyan",
    )
    table.add_column("Flag", footer="Total")
    table.add_column("Count", justify="right", footer=f"{len(flags)}")
    table.add_column("Percent", justify="right", footer=f"{100:.2f}%")

    counter = Counter(flags)
    for item, count in counter.most_common():
        percent = count / len(flags) * 100
        table.add_row(item, f"{count}", f"{percent:.2f}%")

    other_counter = Counter(other_flags)
    if len(counter) < len(other_counter):
        for _ in range(len(other_counter) - len(counter)):
            table.add_row()
    return table


def show_tables(login: str, reviewer: Table, reviewee: Table) -> None:
    console = Console()
    console.print()
    console.print(f"login: [u]{login}[/u]", style="bold")
    console.print()

    table = Table(show_header=False, show_edge=False, box=None)
    table.add_column("1")
    table.add_column("2")
    table.add_row(reviewer, reviewee)

    console.print(table)
    console.print()

from argparse import ArgumentParser, FileType, Namespace


def main() -> None:
    parse_args()


def parse_args() -> None:
    parser = ArgumentParser()
    sub_parser = parser.add_subparsers()

    parser_dump = sub_parser.add_parser("dump", help="Dump json of /v2/scale_teams")
    parser_dump.add_argument("--campus_id", type=int, nargs="*")
    parser_dump.add_argument("--cursus_id", type=int, nargs="*")
    parser_dump.add_argument("--begin_at", type=str, nargs=2, help="filter begin_at")
    parser_dump.set_defaults(func=command_dump)

    parser_count = sub_parser.add_parser(
        "count", help="Count number of review for each login and output csv"
    )
    parser_count.add_argument(
        "json_path", type=FileType("r"), help="json file of scale_teams"
    )
    parser_count.set_defaults(func=command_count)

    parser_visualize = sub_parser.add_parser(
        "visualize", help="Display histogram of number of reviews from correctors.csv"
    )
    parser_visualize.add_argument("csv_path", type=FileType("r"), help="correctors.csv")
    parser_visualize.set_defaults(func=command_visualize)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


def command_dump(args: Namespace) -> None:
    from scale_teams.dump_scale_teams import dump_scale_teams

    dump_scale_teams(args.campus_id, args.cursus_id, args.begin_at)


def command_count(args: Namespace) -> None:
    from scale_teams.count_scale_teams import count_scale_teams

    count_scale_teams(args.json_path)


def command_visualize(args: Namespace) -> None:
    from scale_teams.visualize_scale_teams import visualize_correctors

    visualize_correctors(args.csv_path)


if __name__ == "__main__":
    main()

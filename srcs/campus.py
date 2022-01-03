from argparse import ArgumentParser, FileType, Namespace


def main() -> None:
    parse_args()


def parse_args() -> None:
    parser = ArgumentParser()
    sub_parser = parser.add_subparsers()

    parser_dump = sub_parser.add_parser(
        "dump", help="Dump json of /v2/campus and /v2/cursus_users"
    )
    parser_dump.add_argument("--cursus_id", type=int, nargs="*")
    parser_dump.add_argument("--begin_at", type=str, nargs=2, help="filter begin_at")
    parser_dump.set_defaults(func=command_dump)

    parser_count = sub_parser.add_parser(
        "count", help="Calculate percentage of students absorbed into blackhole"
    )
    parser_count.add_argument(
        "campus_json", type=FileType("r"), help="json file of campus"
    )
    parser_count.add_argument(
        "cursus_users_json",
        type=FileType("r"),
        nargs="*",
        help="json file of cursus_users",
    )
    parser_count.set_defaults(func=command_count)

    parser_visualize = sub_parser.add_parser(
        "visualize",
        help="Display percentage of students absorbed into blackhole and number of students in bar graphs",
    )
    parser_visualize.add_argument(
        "csv_path", type=FileType("r"), help="campus_blackholed.csv"
    )
    parser_visualize.set_defaults(func=command_visualize)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


def command_dump(args: Namespace) -> None:
    from campus.dump_campus import dump_campus_and_cursus_users

    dump_campus_and_cursus_users(args.cursus_id, args.begin_at)


def command_count(args: Namespace) -> None:
    from campus.count_campus import count_cursus_users

    count_cursus_users(args.campus_json, args.cursus_users_json)


def command_visualize(args: Namespace) -> None:
    from campus.visualize_campus import visualize_campus

    visualize_campus(args.csv_path)


if __name__ == "__main__":
    main()

from argparse import ArgumentParser, FileType, Namespace


def main() -> None:
    parse_args()


def parse_args() -> None:
    parser = ArgumentParser()
    sub_parser = parser.add_subparsers()

    parser_dump = sub_parser.add_parser(
        "dump", help="Dump json of /v2/users/:user_id/scale_teams"
    )
    parser_dump.add_argument("login", type=str)
    parser_dump.add_argument("--campus_id", type=int, nargs="*")
    parser_dump.add_argument("--cursus_id", type=int, nargs="*")
    parser_dump.set_defaults(func=command_dump)

    parser_count = sub_parser.add_parser(
        "count", help="Count number of flagged reviews"
    )
    parser_count.add_argument("login", type=str)
    parser_count.add_argument(
        "json_path", type=FileType("r"), help="json file of users_scale_teams"
    )
    parser_count.set_defaults(func=command_count)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


def command_dump(args: Namespace) -> None:
    from user_scale_teams.dump_user_scale_teams import dump_scale_teams

    dump_scale_teams(args.login, args.campus_id, args.cursus_id)


def command_count(args: Namespace) -> None:
    from user_scale_teams.count_user_scale_teams import count_scale_teams

    count_scale_teams(args.login, args.json_path)


if __name__ == "__main__":
    main()

import sys
import argparse
import view.admin_view
import view.pool_view


def main(args: list[str]):
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-p", "--pool", help="manage the pool that is saved in a file")
    group.add_argument(
        "-a", "--admin", action="store_true",
        help="enter the admin mode, manage settings common for all pools")

    parsed_args = parser.parse_args(args[1:])
    args_dict = vars(parsed_args)

    if args_dict["admin"]:
        view.admin_view.admin_view()
    else:
        view.pool_view.pool_view(args_dict["pool"])


if __name__ == "__main__":
    main(sys.argv)

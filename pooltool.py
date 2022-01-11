import sys
import argparse


def main(args: list[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p")
    parser.add_argument("-a", action="store_true")
    parsed_args = parser.parse_args(args[1:])
    _validate_arguments(vars(parsed_args))

    print(parsed_args)


def _validate_arguments(args: dict) -> None:
    if args["p"] and args["a"]:
        raise ValueError("Cannot execute with both -a and -p given.")
    elif not args["p"] and not args["a"]:
        raise ValueError("Cannot launch without any arguments given")


if __name__ == "__main__":
    main(sys.argv)

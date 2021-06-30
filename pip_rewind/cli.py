#! /usr/bin/env python3


import argparse
import sys

from .parser import requirements_parser
from .versions import date_parse, get_first_version_before


def new_requirement(module: str, version: str) -> str:
    return f"{module}=={version}"


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("modules", nargs="*", help="Specify modules to rewind")

    parser.add_argument("-r", "--requirements-file", type=argparse.FileType("r"), help="Use a requirements.txt-formatted file as input")

    parser.add_argument("-d", "--date", type=date_parse, required=True, help="Rewind date, in format MM/DD/YYYY")

    # parser.add_argument("-v", "--verbose", help="Print warnings")

    args = parser.parse_args()

    missing = []

    for module in args.modules:
        version = get_first_version_before(module, args.date)
        if version:
            print(new_requirement(module, version))
        else:
            missing.append(module)

    if args.requirements_file:
        for module in requirements_parser(args.requirements_file):
            version = get_first_version_before(module, args.date)
            if version:
                print(new_requirement(module, version))
            else:
                missing.append(module)

    if missing:
        sys.stderr.write("Previous versions could not be found (from the RSS feed) for:\n")
        for module in missing:
            sys.stderr.write(f"{module} - https://pypi.org/project/{module}/#history")
            sys.stderr.write("\n")

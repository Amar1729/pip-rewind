#! /usr/bin/env python3

"""
Dumb parser for a requirements.txt file.

ONLY supports lines of the following formats:
    (any text can follow the first equality directive)

pkgname==version.number
pkgname<=version.number[...]
pkgname>=version.number[...]
pkgname!=version.number[...]
"""


import re

import warnings
from typing import Generator


def line_parser(line: str) -> str:
    parsed = re.match(r"\s*([A-Za-z0-9\-]+)", line)
    if parsed:
        return parsed.group(1)

    raise Exception(f"{line} - cannot parse requirements object.")


def requirements_parser(f) -> Generator[str, None, None]:
    for line in f.readlines():
        try:
            yield line_parser(line)
        except:
            # warnings.warn(f"{line} - cannot parse requirements object.")
            pass

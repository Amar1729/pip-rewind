#! /usr/bin/env python3

import datetime
from dateutil import parser

from typing import Generator, Optional, Tuple

import requests
import rss_parser
import pytz
from tzlocal import get_localzone


dt = datetime.datetime


def date_parse(date: str) -> dt:
    target_date = parser.parse(date)
    # https://stackoverflow.com/questions/13218506/how-to-get-system-timezone-setting-and-pass-it-to-pytz-timezone
    return target_date.replace(tzinfo=pytz.utc).astimezone(get_localzone())


def get_versions(pkg: str) -> Generator[Tuple[str, datetime.datetime], None, None]:
    rss_url = get_url(pkg)
    xml = requests.get(rss_url)

    feed = rss_parser.Parser(xml=xml.content).parse()

    for item in sorted(feed.feed, key=lambda i: parser.parse(i.publish_date), reverse=True):
        # print(item)
        yield item.title, parser.parse(item.publish_date)


def get_url(pkg: str) -> str:
    # safe name for pkg?
    pkg = pkg.replace("_", "-")
    return f"https://pypi.org/rss/project/{pkg}/releases.xml"


def get_first_version_before_rss(pkg: str, target_date: dt) -> Optional[str]:
    # target_date = parser.parse(date)
    # # https://stackoverflow.com/questions/13218506/how-to-get-system-timezone-setting-and-pass-it-to-pytz-timezone
    # target_date = target_date.replace(tzinfo=pytz.utc).astimezone(get_localzone())

    # assumes get_versions is in order
    for version, release_date in get_versions(pkg):
        if release_date > target_date:
            pass
        else:
            return version

    return None


def get_first_version_before_scraped(pkg: str, date: dt) -> Optional[str]:
    pass


def get_first_version_before(pkg: str, date: dt) -> str:
    version = get_first_version_before_rss(pkg, date)

    if version:
        return version

    version = get_first_version_before_scraped(pkg, date)

    if version:
        return version

    return ""

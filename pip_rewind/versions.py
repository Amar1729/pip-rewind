#! /usr/bin/env python3

import datetime
from dateutil import parser

from typing import Generator, Optional, Tuple

import requests
import rss_parser
import pytz
from result import Ok, Err, Result
from tzlocal import get_localzone


dt = datetime.datetime


def _use_local_tz(date: dt) -> dt:
    # https://stackoverflow.com/questions/13218506/how-to-get-system-timezone-setting-and-pass-it-to-pytz-timezone
    return date.replace(tzinfo=pytz.utc).astimezone(get_localzone())


def date_parse(date: str) -> dt:
    target_date = parser.parse(date)
    return _use_local_tz(target_date)


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


def get_first_version_before_rss(pkg: str, target_date: dt) -> Result[str, str]:
    # target_date = parser.parse(date)
    # # https://stackoverflow.com/questions/13218506/how-to-get-system-timezone-setting-and-pass-it-to-pytz-timezone
    # target_date = target_date.replace(tzinfo=pytz.utc).astimezone(get_localzone())

    # assumes get_versions is in order
    version = ""
    for version, release_date in get_versions(pkg):
        if release_date > target_date:
            pass
        else:
            return Ok(version)

    # return the oldest version we found so the later JSON requests call can use it
    # if version is still empty, then the RSS feed was empty? Not sure how to handle this yet.
    assert version is not None
    return Err(version)


def get_first_version_before_json(pkg: str, version: str, date: dt) -> Result[str, str]:
    """
    Fallback to calling pypi's JSON feed.
    We don't do this first since the URL requires a parameter for version, which
    we don't have until we've parsed at least one version from the XML feed (or
    use HTML scraping).
    """
    url = f"https://pypi.python.org/pypi/{pkg}/{version}/json"
    r = requests.get(url)

    def date_from_release(release) -> dt:
        if release:
            return date_parse(release[0]["upload_time"])
        else:
            # give back unix 0 time if this release has no information
            return _use_local_tz(dt.utcfromtimestamp(0))

    if r.status_code == 200:
        for version, parsed_date in sorted(
            map(
                lambda e: (e[0], date_from_release(e[1])),
                r.json()["releases"].items(),
            ),
            key=lambda e: e[1],
            reverse=True,
        ):
            if parsed_date > date:
                pass
            else:
                return Ok(version)

    # return the oldest version we could find?
    return Err(version)


def get_first_version_before(pkg: str, date: dt) -> str:
    version = get_first_version_before_rss(pkg, date)

    if isinstance(version, Ok):
        return version.value

    version = get_first_version_before_json(pkg, version.value, date)

    return version.value

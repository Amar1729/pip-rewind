# `pip-rewind`

Given a specific date and module names or a requirements.txt-formatted file, this tool can generate a new requirements.txt file with version numbers rewound to what was available on that particular date.

Note - currently, this script only parses the XML RSS feed for a history of each package you pass it, which can be limited. In the future, this script will provide a fallback to HTML-parsing of the pypi history page (which will of course be more likely to break unexpectedly) if the RSS feed does not hold enough history.

## Usage

Note - prone to changes as/if I develop this tool more. See `pip-rewind --help` for more info.

```
$ pip-rewind --date "09/01/2020" requests
```

Or give it a requirements file:

```
$ pip-rewind --date "07/01/2019" -r requirements.txt
```

## Motivation

Starting to work on old projects that don't have **all** their dependencies listed and version-constrained can be difficult (especially when some of those dependencies interact with specific versions of OS packages). The simple existence of a line specifying `redis` in a requirements.txt file without its version can lead to possible breakage when dealing with month- or year-old software.

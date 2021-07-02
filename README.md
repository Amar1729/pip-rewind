# pip-rewind

`pip-rewind` is a command-line tool that can rewind pypi module versions (given as command-line arguments or read from a requirements.txt file) to a previous date in time.

This tool doesn't install any packages itself - rather, it generates output with modules constrained to specific versions, which can then be fed into `pip install`.

## Usage

```
$ pip-rewind --date "09/01/2020" requests > new-requirements.txt
$ pip install -r new-requirements.txt
```

Or give it a requirements file:

```
$ pip-rewind --date "07/01/2019" -r requirements.txt > new-requirements.txt
$ pip install -r new-requirements.txt
```

You can also pipe the output directly to pip if preferred:

```
$ pip-rewind --date "12/01/2020 -r requirements.txt | pip install -r /dev/stdin
```

Currently, this package only parses a simple subset of valid requirements lines:

```
modulename
modulename<=5.0.0
modulename==4.0.0
```

Any line that describes a pypi dependency named `modulename`, possibly with a version identifier after, is valid - this tool simply cares about `modulename` since the version will be rewound anyway. Other lines (such as git dependencies) are ignored.

## Motivation

Starting to work on old projects that don't have **all** their dependencies listed and version-constrained can be difficult (especially when some of those dependencies interact with specific versions of OS packages). The simple existence of a line specifying `redis` in a requirements.txt file without its version can lead to possible breakage when dealing with month- or year-old software.

## LICENSE

MIT

# linkace-cli
A CLI for the API of LinkAce (https://github.com/Kovah/LinkAce)

[![asciicast](https://asciinema.org/a/UO74II9ajDXaNjbwpmxaFdWZX.svg)](https://asciinema.org/a/UO74II9ajDXaNjbwpmxaFdWZX)

![PyPi version](https://pypip.in/v/linkace-cli/badge.png)
![TheJokersThief](https://circleci.com/gh/TheJokersThief/linkace-cli.svg?style=svg)

- [linkace-cli](#linkace-cli)
- [Install](#install)
- [Usage](#usage)
  - [Links](#links)
  - [Lists](#lists)
  - [Tags](#tags)
  - [Search](#search)

# Install

```
pip install linkace-cli
```

# Usage
## Links

```
$ linkace link --help
Usage: linkace link [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create  Create a new link with the info provided.
  delete  Delete a link with the given ID
  get     Get all links or, if --id is provided, get the details of just
          one...

  update  Update a link with the info provided.
```

## Lists

```
$ linkace list --help
Usage: linkace list [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create  Create a new link with the info provided.
  delete  Delete a link with the given ID
  get     Get all lists or, if --id is provided, get the details of just
          one...

  update  Update a list with the info provided.
```

## Tags

```
$ linkace tag --help
Usage: linkace tag [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create  Create a new tag with the info provided.
  delete  Delete a tag with the given ID
  get     Get all tags or, if --id is provided, get the details of just one...
  update  Update a tag with the info provided.
```

## Search

```
$ linkace search --help
Usage: linkace search [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  by-list   Search for links in lists
  by-query  Search for tags by query
  by-tag    Search for links with tags
```

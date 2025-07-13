# PullDocker

[![Travis CI Build Status](https://img.shields.io/travis/com/muflone/pulldocker/main.svg)](https://www.travis-ci.com/github/muflone/pulldocker)
[![CircleCI Build Status](https://img.shields.io/circleci/project/github/muflone/pulldocker/main.svg)](https://circleci.com/gh/muflone/pulldocker)
[![PyPI - Version](https://img.shields.io/pypi/v/PullDocker.svg)](https://pypi.org/project/PullDocker/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/PullDocker.svg)](https://pypi.org/project/PullDocker/)

**Description:** Watch git repositories for Docker compose configuration changes

**Copyright:** 2024-2025 Fabio Castelli (Muflone) <muflone@muflone.com>

**License:** GPL-3+

**Source code:** https://github.com/muflone/pulldocker

**Documentation:** http://www.muflone.com/pulldocker/

## Description

PullDocker is a command line tool monitor a git repository for changes and run
`docker deploy` (and optionally other commands) when changes are detected.

This tool comes handy to automate Docker compose deployments on git operations
(gitops) and can automatically deployments every time a repository receives
updates or a new tag is made.

## System Requirements

* Python >= 3.10
* PyYAML 6.0.x (https://pypi.org/project/PyYAML/)
* GitPython 3.1.x (https://pypi.org/project/GitPython/)

## Usage

PullDocker is a command line utility, so it requires some arguments to be
specified when executing it:

```
pulldocker
  --configuration <YAML FILE>
  [--verbose | --quiet]
  [--watch] [--sleep <SECONDS>]
```

The argument `--configuration` refers to a YAML configuration file containing
repositories' specifications (see below).

The argument `--verbose` will show additional debug messages for diagnostic
purposes.

The argument `--quiet` will hide every diagnostic message showing only errors.

The argument `--watch` will enable the watch mode, continuously checking the
repository for changes.

The argument `--sleep` can specify a number of seconds to await in watch mode
between each iteration.

## YAML Configuration specifications

A YAML configuration file consists of one or more repositories, separated using
`---` and a newline. A repository will require the following minimum arguments:

```yaml
NAME: Repository name
REPOSITORY_DIR: <Path where the git repository is cloned and can be pull>
REMOTES:
  - Remotes list from where to pull the new commits
```

Some more advanced specifications can be found below.

### Minimal example file

```yaml
NAME: PullDocker
REPOSITORY_DIR: /home/muflone/pulldocker.git
REMOTES:
  - origin
```

The previous example would monitor the /home/muflone/pulldocker.git repository,
and it will pull new commits from the remote called `origin`.

Whenever a new commit is found, a new ```docker compose up -d``` command will be
issued in the repository directory.

### Multiple repositories specifications

Multiple repositories can be configured in the same YAML file, and they will be
monitored one after the other, sequentially.

A multi-repository file could be the following:

```yaml
NAME: PullDocker
REPOSITORY_DIR: /home/muflone/pulldocker.git
REMOTES:
  - origin
---
NAME: PixelColor
REPOSITORY_DIR: /home/muflone/pixelcolor.git
REMOTES:
  - github
```

The first repository will monitor the `origin` remote and the second repository
will monitor the `github` remote.

### Complete YAML specifications

Here follows the complete YAML specifications for using PullDocker:

```yaml
NAME: Repository name
REPOSITORY_DIR: <Path where the git repository is cloned and can be pull>
REMOTES:
  - origin
  - github
  - gitlab
TAGS: '*'
COMPOSE_FILE: docker/docker-compose.yaml
COMPOSE_EXEC:
  - docker
  - compose
DETACHED: true
BUILD: true
RECREATE: true
COMMAND: docker compose -f docker/docker-compose.yaml up -d
BEGIN:
  - bash -c 'echo BEGIN ${DATE} ${TIME}'
BEFORE:
  - bash -c 'echo BEFORE ${DATE} ${TIME}'
  - bash -c 'echo ${TAG} ${TAG_HASH} ${TAG_DATE} ${TAG_TIME}'
AFTER:
  - bash -c 'echo AFTER ${DATE} ${TIME}'
  - bash -c 'echo ${TAG} ${TAG_HASH} ${TAG_DATE} ${TAG_TIME}'
END:
  - bash -c 'echo END ${DATE} ${TIME}'
```

The `TAGS` argument can be used to deploy the update only when the latest
commit matches a tag. The tag specification can be `'*'` to indicate any tag
available or a *regex* (Regular expression) can be used to match the available
tags. For example, the following: `TAGS: '0\.[1-9]\.*'` will only match the
tags starting with 0.1.x up to 0.9.x, and it would exclude the tags with 0.0.x.

If no tags are specified, any available commit newer than the current commit
will issue the deployment.

The `COMPOSE_FILE` argument is used to specify the path for a
docker-compose.yaml/yml file in the case the file is contained in another
directory, or it has a different name than the default docker-compose.yaml.

The `COMPOSE_EXEC` argument is used to specify the default `docker compose` to
execute to deploy the container. This defaults to `docker compose` command but
any other command can be specified. Please note this is a **list** of strings,
not a single string.

The `DETACHED` argument is used to specify a boolean value for running the
docker compose in detached mode (the default, passing `true`) or without the
detached mode, by specifying the value `false`.

The `BUILD` argument is used to build the images before starting the
deployment.

The `RECREATE` argument is used to force the recreation of the containers even
if the configuration wasn't changed.

The `PROGRESS` argument is used to enable or disable the progress output
during the deployment.

The `COMMAND` argument can be used to specify the explicit command for the
deployment, instead of using `docker compose up`. This command will override
any previous `COMPOSE_FILE`, `DETACHED`, `BUILD`, `RECREATE`, `PROGRESS`
arguments.

The `BEGIN` argument can be a list of commands to execute when checking the
status for the repository, regardless if it has updates or not.
Multiple commands can be specified.

The `BEFORE` argument can be a list of commands to execute after checking the
status for the repository, before the deployment is done if it **has updates**.
Multiple commands can be specified.

The `AFTER` argument can be a list of commands to execute after checking the
status for the repository, after the deployment is done if it **has updates**.
Multiple commands can be specified.

The `END` argument can be a list of commands to execute after checking the
status for the repository, regardless if it has updates or not.
Multiple commands can be specified.

### Command details

The commands' arguments can use both strings (one command per line) or list of
arguments (one argument per line) using the YAML lists syntax.

The following are both valid:

```yaml
BEGIN:
  - bash -c 'echo BEGIN ${DATE} ${TIME}'
```

Using the list syntax:

```yaml
BEGIN:
  -
    - bash
    - -c
    - 'echo BEGIN ${DATE} ${TIME}'
```

### Command variables

The following special variables can be used in any command to replace the
variable with its value:

- `${NAME}`: repository name in the YAML file
- `${DIRECTORY}`: repository directory path
- `${DATE}`: current date with the format YYYY-MM-DD
- `${TIME}`: current time with the format HH:mm:ss
- `${COMMIT_HASH}`: latest commit hash
- `${COMMIT_DATE}`: latest commit date with the format YYYY-MM-DD
- `${COMMIT_TIME}`: latest commit with the format HH:mm:ss
- `${COMMIT_BRANCH}`: latest commit branch name
- `${COMMIT_AUTHOR}`: latest commit author name
- `${COMMIT_EMAIL}`: latest commit author email
- `${COMMIT_MESSAGE}`: latest commit message
- `${COMMIT_SUMMARY}`: latest commit summary
- `${COMMITS_COUNT}`: number of commits

The following variables can only be used for the `COMMAND`, `BEFORE` and
`AFTER` arguments when the `TAGS` argument is used so their values will refer
to the matching tag used:

- `${TAG}`: tag name
- `${TAG_HASH}`: commit hash for the matching tag
- `${TAG_AUTHOR}`: commit author name for the matching tag
- `${TAG_EMAIL}`: commit author email for the matching tag
- `${TAG_MESSAGE}`: tag message
- `${TAG_SUMMARY}`: commit message for the matching tag
- `${TAG_DATE}`: tag date with the format YYYY-MM-DD
- `${TAG_TIME}`: tag time with the format HH:mm:ss


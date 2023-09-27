# Beerpong

![pytest](https://github.com/juhannc/beerpong/actions/workflows/pytest.yml/badge.svg)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/juhannc/beerpong/main.svg)](https://results.pre-commit.ci/latest/github/juhannc/beerpong/main)
[![codecov](https://codecov.io/gh/juhannc/beerpong/branch/main/graph/badge.svg)](https://codecov.io/gh/juhannc/beerpong)
[![Maintainability](https://api.codeclimate.com/v1/badges/ba14c01e22ad0343af8c/maintainability)](https://codeclimate.com/github/juhannc/beerpong/maintainability)

[![Pypi Status](https://badge.fury.io/py/beerpong.svg)](https://badge.fury.io/py/beerpong)

Bracketing tool with beerpong in mind

## Description

A simple yet powerful bracketing tool with dual window design and beerpong in mind.

## Installation

### End user

Install the most recent stable build via

```shell
pip install beerpong
```

### Developers

Clone the repository via

```shell
git clone https://github.com/juhannc/beerpong.git
```

Afterwards, navigate into the cloned repository and create a install the package via

```shell
python3 -m pip install -e .
```

for basic features.

Or, if you also want to locally run tests, you can use

```shell
python3 -m pip install -e '.[tests]'
```

If you want to have _all_ the dependencies installed, use

```shell
python3 -m pip install -e '.[all]'
```

Finally, to install the pre-commit hooks, run

```shell
pre-commit install
```

Now, prior to any commit, the hooks defined in [`.pre-commit-config.yaml`](./.pre-commit-config.yaml) will be ran.
A failure in any hook will block the commit.
Although, most of the errors, like formatting, will correct themselves.
You just have to re-add all changed files and commit again.

Alternatively, you can run the pipeline at any time to invoke changes before they block commits with

```shell
pre-commit run --all-files
```

## Usage

To run the app, simply use

```shell
beerpong
```

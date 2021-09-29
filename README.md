# Ethereum watcher

Shows blocks and transactions from Ethereum in real-time.

## System Requirements

- Docker https://www.docker.com/
- Docker compose https://docs.docker.com/compose/install/

## Setup

### Setup - Django

```bash
# Copy configuration file
$ cp django/project/env_dist django/project/.env 
```

Change the `ETHERSCAN_API_KEY` for your personal API KEY. You can getting the api key [here](https://docs.etherscan.io/getting-started/viewing-api-usage-statistics).

### Setup - Service containers

```bash
# Build containers
$ ./setup.sh
```
> This script will create a default admin account in Django. User: `admin` pass: `admin`

## How to used

### Start watcher
```bash
$ ./start_watcher.sh
```

> Open this address http://localhost:8000 in a browser tab.

### Stop watcher
```bash
$ ./stop_watcher.sh
```

### Run tests

```bash
$ docker-compose run django pytest
```
## Dependency Management:

- **Poetry**: https://python-poetry.org/

## Dev libraries:

- **Pytest**: https://docs.pytest.org/en/stable/
- **bpython**: https://bpython-interpreter.org/
- **pdbpp**: https://github.com/pdbpp/pdbpp
- **faker**: https://faker.readthedocs.io/en/master/index.html
- **factory-boy**: https://factoryboy.readthedocs.io/en/stable/

## To do list

Thinks to improve, fixes and new features

* Internal transaction support.
* Move VueJs code from html files to JS files
* Web socket support in the index page.
* Complete tests for improve the coverage.
* Ability to scan the entire network, not just the last ones created.
* CLI with [Click library](https://click.palletsprojects.com/en/8.0.x/) for improve the development. Like run tests, build services, etc.
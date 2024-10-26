# Web scraper powered by Robot Framework

Stores the last updated Commander / EDH deck from [Moxfield](https://moxfield.com/decks/public) in [Cockatrice](https://cockatrice.github.io/) format.

## Installation

Compatible with python 3.6 to 3.11

```sh
python -m venv .venv
./.venv/scripts/activate
pip install -r requirements.txt
```

## Usage

```sh
robot -d results .\tests\moxfield-scraper.robot
```

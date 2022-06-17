# Development Notes
## Contents
* [Dependencies](#dependencies)
	* [python-kasa](#python-kasa)
	* [merossiot](#merossiot)
* [Research Tools](#research-tools)

## Dependencies

### python-kasa
Maintenance on this project seems to be somewhat erratic. Because there are a number of different TPLink/Kasa
devices it is hard to test them all. For example, there were a number of issues with the HSL200 3-way switch
that required local changes.

#### Repository
[python-kasa](https://github.com/python-kasa/python-kasa)

#### Tools Used
This package uses the [Poetry](https://python-poetry.org/) dependency management app. 
Under macOS you can use brew to install Poetry.

```
brew install poetry
```

##### Install all development tools
```
poetry install
```
Note that his installs a large number of tools. It is not suitable for a production environment.

##### Build a PIP installable

```
poetry build
```
This will build a .gz and .whl file in the dist directory. Either of these files can be copied to
another system and installed with PIP.

```
pip install /Users/username/Source/python-kasa/dist/python_kasa-0.4.0.dev3-py3-none-any.whl
```

### merossiot

#### Repository
[Meross Python Library](https://github.com/albertogeniola/MerossIot)

## Research Tools
These scripts can be used to explore different devices.

* meross\_asyncio\_test.py* meross\_bulb\_test.py* meross\_test.py* tplink\_test.py


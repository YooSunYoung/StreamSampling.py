# Getting started

## Setting up

### Dependencies

Development dependencies are specified in `pixi.lock` so you can install the dependencies with pixi command.

```sh
pixi install --frozen  # Frozen flag means it will not update the lock file and install the dependencies as it says.
```

Additionally, building the documentation requires [pandoc](https://pandoc.org/) which is not on PyPI and needs to be installed through other means, e.g. with your OS package manager.

### Install the package

The lock file should already have the path to the package to be installed in editable mode.

```toml
streamsampling = { path = "src", editable = true, extras = ["test"] }
```

### Set up git hooks

The CI pipeline runs a number of code formatting and static analysis tools.
If they fail, a build is rejected.
To avoid that, you can run the same tools locally.
This can be done conveniently using [pre-commit](https://pre-commit.com/) or [prek](https://prek.j178.dev/):

```sh
pre-commit install
# or
prek install
```

Alternatively, if you want a different workflow, take a look at ``.pre-commit.yaml`` and ``pyproject.toml`` to see what tools are run and how.

## Running tests

`````{tab-set}
````{tab-item} pixi test
Run the tests using

```sh
pixi test
```

````
`````

## Building the docs

`````{tab-set}
````{tab-item} pixi docs
Build the documentation using

```sh
pixi run docs
```

This builds the docs and also runs `doctest`.
`linkcheck` can be run separately using

```sh
pixi run linkcheck
```
````

````{tab-item} Manually

Build the documentation using

```sh
python -m sphinx -v -b html -d .tox/docs_doctrees docs html
```

Additionally, test the documentation using

```sh
python -m sphinx -v -b doctest -d .tox/docs_doctrees docs html
python -m sphinx -v -b linkcheck -d .tox/docs_doctrees docs html
```
````
`````

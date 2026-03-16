# Dependency management

streamsampling is a library, so the package dependencies are never pinned.
Lower bounds are fine and individual versions can be excluded.
See, e.g., [Should You Use Upper Bound Version Constraints](https://iscinumpy.dev/post/bound-version-constraints/) for an explanation.

Development dependencies (as opposed to dependencies of the deployed package that users need to install) are pinned to an exact version in order to ensure reproducibility.
This also includes dependencies used for the various CI builds.
This is done by specifying packages in `pixi.lock` file and locking those dependencies using [pixi](https://pixi.prefix.dev/latest/).
Various environments and tasks are defined in `pixi.toml` file.


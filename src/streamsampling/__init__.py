# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2026 Yoosunyoung contributors (https://github.com/yoosunyoung)
# ruff: noqa: RUF100, E402, F401, I

import importlib.metadata

try:
    __version__ = importlib.metadata.version(__package__ or __name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"

del importlib

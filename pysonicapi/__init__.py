# -*- coding: utf-8 -*-
""" The root of SonicOS package namespace."""

try:
    import pkg_resources

    __version__ = pkg_resources.get_distribution("pysonicapi").version
except Exception:
    __version__ = "unknown"

from pysonicapi.pysonicapi import SonicWall

__all__ = (
    "SonicWall",
)
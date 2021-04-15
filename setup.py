#!/usr/bin/env python3

from setuptools import setup

setup(
    name="radicale-share-collections",
    version="0.1",
    description="""Hack to make radicale collections discoverable
for users who have read access""",
    author="Finn Krein",
    license="GNU AGPL v3",
    install_requires=["radicale >= 3.0"],
    packages=["radicale_share_collections"],
    entry_points={
        "console_scripts": [
            "radicale_share_collections = radicale_share_collections.__main__:main"
        ]
    }
)

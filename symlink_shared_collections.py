#!/usr/bin/python3

from argparse import ArgumentParser
from os import path, scandir, symlink, unlink
import radicale


def visible_subdirs(path):
    return [
        p.name for p in scandir(path)
        if not p.name.startswith(".") and p.is_dir() and not p.is_symlink()
    ]


def symlink_shared_collections(storepath, rights):
    users = visible_subdirs(storepath)
    for owner in users:
        for collection in visible_subdirs(path.join(storepath, owner)):
            collection_path = path.join(owner, collection)
            collection_dir = path.join(storepath, collection_path)
            for user in users:
                has_read = rights.authorized(user, collection_path, "r")
                destination = path.join(storepath, user, collection)
                if has_read:
                    if path.exists(destination):
                        continue
                    else:
                        symlink(collection_dir, destination)
                else:
                    if path.islink(destination):
                        unlink(destination)


def main():
    parser = ArgumentParser(
        """Hack to make shared radicale collections visible
        to every user who has read access to the collection."""
    )
    parser.add_argument("config", help="radicale config")
    args = parser.parse_args()

    config = radicale.config.load([args.config])
    storepath = path.join(config.get("storage", "filesystem_folder"),
                          "collection-root")
    radicale_users = visible_subdirs(storepath)
    logger = radicale.log.start("radicale", config.get("logging", "config"))
    rights = radicale.rights.load(config, logger)
    symlink_shared_collections(storepath, rights)


if __name__ == "__main__":
    main()

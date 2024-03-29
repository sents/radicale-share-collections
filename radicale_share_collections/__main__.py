#!/usr/bin/python3

from argparse import ArgumentParser
from os import path, listdir, scandir, symlink, unlink
import radicale


def visible_subdirs(path):
    return [
        p.name
        for p in scandir(path)
        if not p.name.startswith(".") and p.is_dir() and not p.is_symlink()
    ]


def symlink_shared_collections(storepath, rights, owner, collection, users):
    collection_path = path.join(owner, collection)
    collection_dir = path.join(storepath, collection_path)
    for user in users.difference({owner}):
        has_read = 'r' in rights.authorization(user, f"/{collection_path}")
        destination = path.join(storepath, user, f"from-{owner}-{collection}")
        if has_read and not path.exists(destination):
            symlink(collection_dir, destination)
        elif not has_read and path.islink(destination):
            unlink(destination)


def delete_broken_symlinks(collection_path):
    # find broken symlinks and unlink them
    with scandir(collection_path) as dirit:
        for link in dirit:
            if link.is_symlink() and not path.exists(link):
                unlink(link.path)


def manage_symlinks(storepath, rights, collections, users):
    for owner in collections:
        delete_broken_symlinks(path.join(storepath, owner))
        for collection in visible_subdirs(path.join(storepath, owner)):
            symlink_shared_collections(storepath,
                                       rights,
                                       owner,
                                       collection,
                                       users)


def main():
    parser = ArgumentParser(
        """Hack to make shared radicale collections visible
to every user who has read access to the collection.
"""
    )
    parser.add_argument("config", help="path to Radicale config")
    parser.add_argument(
        "-u",
        "--users",
        default=None,
        help="""
Users for which to run the script; If not specified,
the script is run for all users.""",
    )
    parser.add_argument(
        "-c",
        "--collections",
        default=None,
        help="""
Collections for which to run the script; If not specified the script is run on
all collections.""",
    )
    args = parser.parse_args()

    config = radicale.config.load([(args.config, False)])
    storepath = path.join(config.get("storage",
                                     "filesystem_folder"),
                          "collection-root")
    rights = radicale.rights.load(config)
    primary_collections = set(visible_subdirs(storepath))
    if args.users is None:
        users = primary_collections
    else:
        users = set(args.users.strip(",").split(",")).intersection(
            primary_collections
        )
    if args.collections is None:
        collections = primary_collections
    else:
        collections = set(args.collections.strip(",").split(",")).intersection(
            primary_collections
        )
    manage_symlinks(storepath, rights, collections, users)


if __name__ == "__main__":
    main()

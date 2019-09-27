#!/usr/bin/python3

from os import path, scandir, symlink
import radicale


def visible_subdirs(path):
    return [p.name
            for p in scandir(path)
            if not p.name.startswith(".") and p.is_dir()]


def symlink_shared_collections(storepath, rights):
    users = visible_subdirs(storepath)
    for owner in users:
        for collection in visible_subdirs(path.join(storepath, owner)):
            collection_path = path.join(storepath, owner, collection)
            for user in users:
                has_read = rights.authorized(user, collection_path, "r")
                destination = path.join(storepath, user, collection)
                if has_read:
                    if path.exists(destination):
                        continue
                    else:
                        symlink(collection_path, destination)
                else:
                    if path.exists(destination) and path.islink(destination):
                        os.unlink(destination)


def main():
    config = radicale.config.load(["/etc/radicale/config"])
    storepath = path.join(config.get("storage", "filesystem_folder"),
                          "collection-root")
    radicale_users = visible_subdirs(storepath)
    logger = radicale.log.start("radicale", config.get("logging", "config"))
    rights = radicale.rights.load(configuration, logger)
    symlink_shared_collections(storepath, rights)


if __name__ == "__main__":
    main()

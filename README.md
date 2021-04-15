# What does this do?
This python package provides a script that can be used to
symlink Radicale collections into the path of all users, that
have read access to that collection. Effectively this makes collections
which are not owned but readable to a user discoverable in the Radicale
web interface and in any CalDav client.

For this to work the `multifilesystem` storage backend for Radicale has to be used.

This script is only compatible with Radicale 3.

The package also provides templates for systemd service and timer files to run
the script periodically.

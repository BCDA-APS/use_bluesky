#!/usr/bin/env python

"""
create an instrument package template in a .tar.gz file
"""

import os
import shutil
import sys
import tarfile
import tempfile


def main():
    local_path = os.path.dirname(__file__)
    pkg_path = os.path.abspath(os.path.join(local_path, ".."))
    src_path = os.path.join(pkg_path, "lessons", "instrument")
    temp_path = tempfile.mkdtemp()

    # copy src_path to subdir of temp_path
    dest = os.path.join(temp_path, "instrument")
    shutil.copytree(src_path, dest)

    # edit temp_path/instrument
    rm_paths = [
        ["instrument", "__pycache__"],
        ["instrument", "callbacks", "ideas"],
        ["instrument", "callbacks", "__pycache__"],
        ["instrument", "devices", "__pycache__"],
        ["instrument", "devices", "ideas"],
        ["instrument", "devices", "TODO"],
        ["instrument", "framework", "__pycache__"],
        ["instrument", "mpl", "__pycache__"],
        ["instrument", "plans", "__pycache__"],
        ["instrument", "plans", "ideas"],
        ["instrument", "utils", "__pycache__"],
    ]
    for path in rm_paths:
        shutil.rmtree(os.path.join(temp_path, *path), ignore_errors=True)

    # add temp_path/00-instrument.py
    shutil.copy2(
        os.path.join(pkg_path, "templates", "example_00-instrument.py"),
        os.path.join(temp_path, "00-instrument.py"))

    # add temp_path/setup.py
    shutil.copy2(
        os.path.join(pkg_path, "templates", "example_setup.py"),
        os.path.join(temp_path, "setup.py"))

    # copy pkg_path/templates/blueskyStarter.sh to temp_path
    shutil.copy2(
        os.path.join(pkg_path, "templates", "example_blueskyStarter.sh"),
        os.path.join(temp_path, "blueskyStarter.sh"))

    # create archive file instrument.tar.gz
    fname = os.path.join(local_path, "example_instrument.tar.gz")
    with tarfile.open(fname, "w:gz") as tar:
        tar.add(temp_path, arcname="instrument_template")

    if os.path.exists(temp_path):
        shutil.rmtree(temp_path, ignore_errors=True)

    print(f"created file: {fname}")


if __name__ == "__main__":
    main()

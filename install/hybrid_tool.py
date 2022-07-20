#!/usr/bin/env python

"""
Tool used in support of hybrid_installer.sh
"""

import argparse
import sys
import ruamel_yaml as yaml


def read_yml(env_file):
    # print(f"{env_file}")
    with open(env_file, "r") as f:
        all_specs = yaml.safe_load(f)
    return all_specs


def get_pip_requirements(specs):
    for item in specs["dependencies"]:
        # print(item)
        if isinstance(item, dict):
            reqs = item.get("pip")
            if reqs is not None:
                print("\n".join(sorted(reqs)))


def get_conda_requirements(specs):
    pass


def get_environment_name(specs):
    print(specs["name"])


def get_user_parameters():
    parser = argparse.ArgumentParser(prog="hybrid_tool",)
    parser.add_argument(
        "function", action="store", help="one of: name, pip, conda"
    )
    parser.add_argument(
        "env_file", action="store", help="environment YAML file"
    )
    return parser.parse_args()


def main():
    args = get_user_parameters()
    all_specs = read_yml(args.env_file)
    func = dict(
        conda=get_pip_requirements,
        name=get_environment_name,
        pip=get_pip_requirements,
    )[args.function](read_yml(args.env_file))


if __name__ == "__main__":
    main()

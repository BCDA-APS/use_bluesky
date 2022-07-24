#!/usr/bin/env python

"""
Tool used in support of hybrid_installer.sh
"""

import argparse
try:
    import ruamel_yaml as yaml
except ModuleNotFoundError:
    import yaml


def read_yml(env_file):
    # print(f"{env_file}")
    with open(env_file, "r") as f:
        all_specs = yaml.safe_load(f)
    return all_specs


def print_pip_requirements(specs):
    for req in specs["dependencies"]:
        # print(req)
        if isinstance(req, dict):
            reqs = req.get("pip")
            if reqs is not None:
                print("\n".join(sorted(reqs)))


def print_conda_requirements(specs):
    pass  # TODO: but not needed


def print_environment_name(specs):
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
    func = dict(
        conda=print_pip_requirements,
        name=print_environment_name,
        pip=print_pip_requirements,
    )[args.function]
    func(read_yml(args.env_file))


if __name__ == "__main__":
    # import sys
    # sys.argv.append("pip")
    # sys.argv.append("./install/test.yml")
    main()

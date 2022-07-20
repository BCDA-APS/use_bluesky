#!/usr/bin/env python

"""
Tool used in support of hybrid_installer.sh
"""

import argparse
import sys
import ruamel_yaml as yaml

def main():
    env_file = sys.argv[1]
    print(f"{env_file}")
    with open(env_file, "r") as f:
        all_specs = yaml.safe_load(f)
    print(f"{all_specs}")


if __name__ == "__main__":
    main()

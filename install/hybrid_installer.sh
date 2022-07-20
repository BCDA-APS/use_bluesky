#!/bin/bash

# purpose: hybrid conda environment installer

function usage {
    echo "usage: ${0} [-y] [-n env_name] env_file.yml"
    # TODO: explain
    exit
}

# ----- parse command line inputs

UMAMBA=$(which micromamba)
CONDA=$(which conda)

if [ "${UMAMBA}" == "" ]; then
    echo "Cannot identify micromamba executable."
    exit
fi
if [ "${CONDA}" == "" ]; then
    echo "Cannot identify conda executable."
    exit
fi

environment=
yml_file=
options=
while [ -n "$1" ]; do
    case "${1}" in
        -y) options+=" ${1}" ;;
        -n)
            if [ "${environment}" == "" ]; then
                environment=${2}
                shift
            else
                usage
            fi
            ;;
        *)
            if [ "${yml_file}" == "" ]; then
                yml_file=${1}
            else
                usage
            fi
            ;;
    esac
    shift
done

if [ -e "${yml_file}" ]; then
    if [ "${environment}" == "" ]; then
        match=$(grep name: "${yml_file}")
        sarray=($match)
        environment=${sarray[1]}
    fi
else
    usage
fi

# echo environment=${environment}
# echo options=${options}
# echo yml_file=${yml_file}
echo "create ${options} -n ${environment} ${yml_file}"

# ----- build test micromamba environment

temp_env=env_$(date "+%H%M%S")
# echo temp_env=${temp_env}
micromamba create -n "${temp_env}" -f "${yml_file}"

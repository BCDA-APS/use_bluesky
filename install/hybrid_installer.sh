#!/bin/bash

# purpose: hybrid conda environment installer

function usage {
    echo "usage: ${0} [-y] [-n env_name] env_file.yml"
    # TODO: explain
    exit
}

# ----- 1. accepts an environment file name and optional environment name

PYTOOL=./hybrid_tool.py
if [ "$(which micromamba)" == "" ]; then
    echo "Cannot identify micromamba executable."
    exit
fi
if [ "$(which conda)" == "" ]; then
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
        environment=$(${PYTOOL} name "${yml_file}")
    fi
else
    usage
fi

# echo environment=${environment}
# echo options=${options}
# echo yml_file=${yml_file}
echo "create ${options} -n ${environment} ${yml_file}"

# ----- 2. build test micromamba environment

TIMEDATE=$(date "+%H%M%S")
temp_env="hybrid_env_${TIMEDATE}"
# echo temp_env=${temp_env}
micromamba create -n "${temp_env}" -f "${yml_file}"
eval "$(micromamba shell hook --shell=bash)"
micromamba activate "${temp_env}"
# micromamba env list

# ----- 3. create a pip requirements file from the input environment file

pip_req_file="/tmp/${TIMEDATE}_pip_req.txt"
# FIXME: does not write the file yet
${PYTOOL} pip "${yml_file}" | tee "${pip_req_file}"

# ----- 4. generate the explicit package list for conda

conda_explicit_file="/tmp/${TIMEDATE}_conda_explicit.txt"
conda list --explicit | tee "${conda_explicit_file}"

# ----- 5. remove the test micromamba environment
# ----- 6. create named conda environment with the explicit list
# conda create --name <env> --file <this file>
# ----- 7. pip install remaining components in the named conda environment
# ----- 8. remove pip requirements file and conda explicit file

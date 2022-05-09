#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
RU_TMPL_DIR="$BASEDIR/localisation/"

# Some useful colors.
if [[ -z "${color_start-}" ]]; then
    declare -r color_start="\033["
    declare -r color_red="${color_start}0;31m"
    declare -r color_yellow="${color_start}0;33m"
    declare -r color_green="${color_start}0;32m"
    declare -r color_norm="${color_start}0m"
fi

function logr {
    echo -e "${color_red}$1${color_norm}" 1>&2
}
function logy {
    echo -e "${color_yellow}$1${color_norm}" 1>&2
}
function log {
    echo -e "${color_green}$1${color_norm}" 1>&2
}
function die {
    logr "$1"
    exit 1
}

function main () {
  echo "Orig dir: $1"
  if [[ ! -z $2 ]]; then
      echo "Target dir: $2"
      RU_TMPL_DIR=$2
  fi
  TARGET_DIR=$1
  orig_files_no_loc=$(ls "$TARGET_DIR" | sed "s/_l_english.yml//g")
  for i in $orig_files_no_loc
  do
    python3 "$BASEDIR"/localize.py "$TARGET_DIR"/"$i"_l_english.yml "$RU_TMPL_DIR"/"$i"_l_russian.yml
  done
}

main "$@"
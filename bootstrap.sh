#!/usr/bin/env bash

cd "`dirname "${BASH_SOURCE[0]}"`" >/dev/null 2>&1


main () {
  package=$1
  title=`echo ${package/_/ } | sed 's/\S*/\u&/g'`
  # replace
  find . -type f | while IFS= read -r f; do
    sed -i -e "s/{TITLE}/${title}/g" -e "s/{PACKAGE}/${package}/g" $f
  done
  # package dir
  mv PACKAGE $package
  mv _README.md README.md
  rm bootstrap.sh
}

read -p $'Input the Python package name of your project, e.g.: my_project\n'
main $REPLY

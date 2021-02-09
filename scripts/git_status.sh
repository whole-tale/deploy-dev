#!/bin/bash

for dir in $(find src/ -maxdepth 1 -mindepth 1 -type d | sort) ; do \
  pushd $dir &> /dev/null
  dirty=""
  [[ $(git status 2> /dev/null | tail -n1) == *"nothing to commit"* ]] && dirty='*'
  branch=$(git rev-parse --abbrev-ref HEAD)
  echo "${dir}" "[${branch}${dirty}]"
  popd &> /dev/null
done

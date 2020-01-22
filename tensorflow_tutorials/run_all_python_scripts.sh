#!/usr/bin/env bash
echo "python interpreter is $(which python)"
echo "current working directory is $(pwd)"

if [ $(pwd) != $(dirname "$0") ]
then
  echo '[Error] the script is supposed to run from its residing directory.'
  echo '[Info] Exiting without doing anything else.'
  exit 1
fi

find . -mindepth 2 -regex ".*\.py$" -print0 | xargs -0 -i sh -c  \
  "echo '[Info] begin to run {}'; \
   python {}; if [ $? -ne 0 ]; then exit $?; \
   else echo '[Info] finished running {}. exit code is $?'; fi"

echo '[Info] all python scripts finished successfully.'
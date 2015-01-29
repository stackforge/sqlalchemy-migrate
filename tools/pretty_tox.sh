#!/usr/bin/env bash

# return nonzero exit status of rightmost command, so that we
# get nonzero exit on test failure without halting subunit-trace
set -o pipefail


TESTRARGS=$1

python setup.py testr --testr-args="--subunit $TESTRARGS  --concurrency=1" | subunit-trace -f
retval=$?
# NOTE(mtreinish) The pipe above would eat the slowest display from pbr's testr
# wrapper so just manually print the slowest tests
echo -e "\nSlowest Tests:\n"
testr slowest
exit $retval

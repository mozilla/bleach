#!/usr/bin/env python

"""
Util to write bleach .test and .test.out files to the CWD from the
DOMPurify expect.js fixture file provided via stdin.

Example:

cat expect.js | python tests/dompurify_fixture_to_data.py --start-index 20
ls -l
20.test
20.test.out

"""

import argparse
import json
import os
import os.path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--start-index',
                        type=int,
                        default=1,
                        help='index to start writing test files from.')

    args = parser.parse_args()

    cases = sys.stdin.read()

    # drop JS module wrapping
    cases = cases.replace('module.exports = ', '', 1).rstrip().rstrip(';')

    cases = cases.replace('\\u', '\\\\u')

    for i, case in enumerate(json.loads(cases), args.start_index):
        print(i, case['payload'], case['expected'])

        with open('%d.test' % i, 'a') as test_inf:
            test_inf.write(case['payload'] + '\n')

        with open('%d.test.out' % i, 'a') as test_outf:
            if type(case['expected']) == str:
                test_outf.write(case['expected'] + '\n')
            elif type(case['expected']) == list:
                test_outf.write(case['expected'][0] + '\n')
            else:
                raise Exception("Unexpected testcase output type: %s" % type(case['expected']))

if __name__ == '__main__':
    main()
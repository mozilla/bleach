#!/usr/bin/env python

"""
Util to write a directory of test cases with input filenames
<testcase>.test as JSON to stdout.

example::

    $ python tests/data_to_json.py tests/data > testcases.json

"""

import argparse
import fnmatch
import json
import os
import os.path

import bleach


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'data_dir',
        help=(
            'directory containing test cases with names like <testcase>.test'
        )
    )

    args = parser.parse_args()

    filenames = os.listdir(args.data_dir)
    ins = [os.path.join(args.data_dir, f) for f in filenames if fnmatch.fnmatch(f, '*.test')]

    testcases = []
    for infn in ins:
        case_name = infn.rsplit('.test', 1)[0]

        with open(infn, 'r') as fin:
            data, expected = fin.read().split('\n--\n')
            data = data.strip()
            expected = expected.strip()

            testcases.append({
                'title': case_name,
                'input_filename': infn,
                'payload': data,
                'actual': bleach.clean(data),
                'expected': expected,
            })

    print(json.dumps(testcases, indent=4, sort_keys=True))


if __name__ == '__main__':
    main()

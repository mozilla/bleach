#!/usr/bin/env python

"""
Util to write a directory of test cases with input filenames
<testcase>.test and output filenames <testcase>.test.out as JSON to
stdout.

example:

python tests/data_to_json.py tests/data > testcases.json
"""

import argparse
import fnmatch
import json
import os
import os.path

import bleach


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('data_dir',
                        help='directory containing test cases with input files'
                        ' named <testcase>.test and output <testcase>.test.out')

    args = parser.parse_args()

    filenames = os.listdir(args.data_dir)
    ins = [os.path.join(args.data_dir, f) for f in filenames if fnmatch.fnmatch(f, '*.test')]
    outs = [os.path.join(args.data_dir, f) for f in filenames if fnmatch.fnmatch(f, '*.test.out')]

    testcases = []
    for infn, outfn in zip(ins, outs):
        case_name = infn.rsplit('.test', 1)[0]

        with open(infn, 'r') as fin, open(outfn, 'r') as fout:
            payload = fin.read()[:-1]
            testcases.append({
                "title": case_name,
                "input_filename": infn,
                "output_filename": outfn,
                "payload": payload,
                "actual": bleach.clean(payload),
                "expected": fout.read(),
            })

    print(json.dumps(testcases, indent=4, sort_keys=True))


if __name__ == '__main__':
    main()

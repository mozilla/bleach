# -*- coding: utf-8 -*-
'''
Parse public suffix list and generate suffix regular expression

Usage: python suffix_update.py bleach/suffix.py

It will fetch public suffix list from
"https://publicsuffix.org/list/public_suffix_list.dat" and
generate python script contains suffix regular expression into
"bleach/sffix.py"

To see detail usage, please run "python suffix_update.py --help".

This script use `argparse`. To run this script need python > 2.6.
'''
from __future__ import unicode_literals
import sys
is_py_2 = sys.version_info[0] == 2
if is_py_2:
    # for python 2.x
    from StringIO import StringIO
    from codecs import open as open_with_codec
    from codecs import getwriter
else:
    # for python 3.x
    from io import StringIO
    open_with_codec = open


def read_suffix_list(contents):
    '''
    Read and parse suffix list.
    '''
    # remove comment & blank line
    suffix_list = [line.lower().strip()
                   for line in contents
                   if not line.startswith('//') and line.strip()]

    # find idna decodable suffixs
    idna_encoded_suffix_list = []
    for suffix in suffix_list:
        try:
            encoded = suffix.encode('idna').decode('ascii')
            if suffix != encoded:
                idna_encoded_suffix_list.append(encoded)
        except UnicodeDecodeError:
            # When unicode decode error occured...
            # ignore it.
            pass

    idna_encoded_suffix_list.sort()
    # extend idna encoded suffix_list
    suffix_list.extend(idna_encoded_suffix_list)

    suffix_list.sort()

    return suffix_list


def write_suffix_py(out, suffix_list):
    '''
    Write suffix list as python source.
    '''
    out.write("# -*- coding: utf-8 -*-\n"
              "from __future__ import unicode_literals\n\n")

    def write(var_begin, suffix_lst, end, line_acc, process, process_elem):
        '''
        write suffix list with pep8 rule.
        - 80col rule
        - auto indent
        '''
        first_line_max_length = 79 - len(var_begin)
        line_max_length = first_line_max_length
        one_line_max_length = first_line_max_length
        count, tmp, indent = 0, [], 0
        out.write(var_begin)
        if suffix_lst:
            for suffix in suffix_lst:
                processed_elem, length = process_elem(suffix)
                length += len(processed_elem)
                if count + len(processed_elem) + line_acc >= line_max_length:
                    out.write((' ' * indent + process(tmp, indent == 0)))
                    out.write('\n')
                    tmp, count, indent = [], 0, len(var_begin)
                    line_max_length = one_line_max_length
                tmp.append(processed_elem)
                count += length
            if tmp:
                out.write(' ' * indent + process(tmp, indent == 0))
        else:
            # write empty string
            out.write("''")
        out.write(end)

    import re

    suffix_re_list = []
    exceptional_domain_re_list = []
    for suffix in suffix_list:
        ''' make suffix to regular expression
            1. replace `.` to `\\.`
            2. special suffix rules.
                - see https://publicsuffix.org/list/#list-format
        '''

        suffix = suffix.replace('.', '\\.')
        suffix = re.sub(r'\*\\\.', '', suffix)
        # exceptional case
        # this is not a suffix. It can be a whole domain.
        if suffix.startswith('!'):
            suffix = suffix[1:]
            exceptional_domain_re_list.append(suffix)
            continue
        suffix_re_list.append(suffix)

    suffix_re_list.sort()
    suffix_re_list.reverse()

    exceptional_domain_re_list.sort()
    exceptional_domain_re_list.reverse()

    # write public suffixes Regular Expression.
    # it can be only suffix. need more level for this cases.
    # ex) com -> not accepted
    #     example.com -> accepted
    write('SUFFIXES_RE = (', suffix_re_list, ')', 3,
          lambda x, f: ('"%s"' if f else '"|%s"') % '|'.join(x),
          lambda x: (x, 1))
    out.write('\n\n')

    # write exceptional domain regular expression.
    # it can be whole domain.
    write('EXCEPTIONAL_DOMAIN_RE = (', exceptional_domain_re_list, ')', 3,
          lambda x, f: ('"%s"' if f else '"|%s"') % '|'.join(x),
          lambda x: (x, 1))
    out.write('\n')

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Parse public suffix list"
                            " and write as python source",
                            usage="python suffix_update.py bleach/suffix.py")
    parser.add_argument("-f", dest="filename", help="Read from file. if this "
                        "value is not set, get public suffix list from 'https:"
                        "//publicsuffix.org/list/public_suffix_list.dat'",
                        default=None)
    parser.add_argument("output", help="output filename."
                        " or '-' to stdout")

    args = parser.parse_args()

    if not args.filename:
        # get suffix list from
        # https://publicsuffix.org/list/public_suffix_list.dat
        if is_py_2:
            # for python 2.x
            from httplib import HTTPSConnection
        else:
            # for python 3.x
            from http.client import HTTPSConnection
        connection = HTTPSConnection('publicsuffix.org')
        connection.request('GET', '/list/public_suffix_list.dat')
        response = connection.getresponse()

        contents = StringIO(response.read().decode('utf-8'))
    else:
        contents = open_with_codec(args.filename, "r", encoding="utf-8")

    suffix_list = read_suffix_list(contents)
    contents.close()

    if args.output == '-':
        # use stdout
        from sys import stdout
        if is_py_2:
            out = getwriter('utf-8')(stdout)
        else:
            out = stdout
    else:
        out = open_with_codec(args.output, "w", encoding="utf-8")

    write_suffix_py(out, suffix_list)
    out.close()

# tests...
from nose.tools import eq_


def test_read_list():
    '''
    test for read_suffix_list function.
    '''

    # input, expected result
    cases = (
        ('', []),  # empty
        ('com', sorted(['com'])),  # basic single
        ('com' '\n'
         'net', sorted(['com', 'net'])),  # basic multiple
        ('*.com' '\n'
         '!example.com', sorted(['*.com', '!example.com'])),  # special case
        ('// this is comment', []),  # comment only
        ('com' '\n'
         '// bd : http://en.wikipedia.org/wiki/.bd' '\n'
         '*.bd', sorted(['com', '*.bd'])),  # comment with others
        ('\n'
         '\n'
         'com' '\n'
         'net' '\n', sorted(['com', 'net'])),  # empty lines
        ('   ', sorted([])),  # whitespaces
        ('한국', sorted(['한국', 'xn--3e0b707e'])),  # unicode
    )

    for case in cases:
        out = read_suffix_list(StringIO(case[0]))
        eq_(out, case[1])


def test_re_gen():
    '''
    test for function write_suffix_py
    '''
    from tempfile import mkstemp
    from imp import load_module, find_module
    from flake8.engine import get_style_guide
    from os.path import split as path_split, splitext

    def check_file(path, ignore=(), complexity=-1):
        ''' From flake8.main
        flake8.main needs setuptools which not required for here
        and it occurs error on python 2.7, OSX'''
        ignore = set(ignore)
        flake8_style = get_style_guide(ignore=ignore,
                                       max_complexity=complexity)
        return flake8_style.input_file(path)

    # input, expected SUFFIX_RE, expected EXCEPTIONAL_DOMAIN_RE
    cases = (
        (['com'], 'com', ''),  # basic case
        (['com', 'net'], 'net|com', ''),  # basic case 2 - order
        (['ac.cr'], 'ac\\.cr', ''),  # escape '.'
        (['*.com', '!example.com'], 'com', 'example\\.com'),  # special case
        (['الجزائر', 'الاردن', 'ارامكو', 'اتصالات', 'ابوظبي', 'קום',
          'ירושלים\.museum', 'հայ', 'қаз', 'упр\.срб', 'укр'],
         'الجزائر|الاردن|ارامكو|اتصالات|ابوظبي|קום|ירושלים\.museum|հայ|қаз'
         '|упр\.срб|укр', ''),
        # long input with unicode- flake8 check
    )

    for case in cases:
        temp_file_path = mkstemp('.py')[1]
        with open_with_codec(temp_file_path, "w", encoding="utf-8") as out:
            # save generated source file and load it.
            write_suffix_py(out, case[0])
            # flush file to load as module
            out.flush()

            # check flake8 rule
            check_file(out.name)

            file_dir, file_name = path_split(temp_file_path)
            file_name, ext = splitext(file_name)

            # test generated regular expression
            fp, path, desc = find_module(file_name, [file_dir])
            re_module = load_module(file_name, fp, path, desc)
            eq_(re_module.SUFFIXES_RE, case[1])
            eq_(re_module.EXCEPTIONAL_DOMAIN_RE, case[2])

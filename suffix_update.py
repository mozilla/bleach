import sys
is_py_2 = sys.version_info[0] == 2


def read_suffix_list(content):
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
        first_line_max_length = 79 - len(var_begin)
        line_max_length = first_line_max_length
        one_line_max_length = first_line_max_length
        count, tmp, indent = 0, [], 0
        out.write(var_begin)
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
        out.write(end)

    # Write suffixes list.
    #
    # write('SUFFIXES = [', suffix_list, ' ]', 1,
    #       lambda x, f: ', '.join(x) + ',',
    #       lambda x: ('"%s"' % x, 2))

    # out.write('\n\n')

    # write public suffixes Regular Expression.
    suffix_list = list(map(lambda x: x.replace('.', '\\.')
                           .replace('*', '[^.]+').replace('!', ''),
                           suffix_list))
    suffix_list.sort()
    suffix_list.reverse()
    write('SUFFIXES_RE = (', suffix_list, ')', 3,
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

    if is_py_2:
        from codecs import open as open_with_codec
        from codecs import getwriter
    else:
        open_with_codec = open

    if not args.filename:
        # get suffix list from
        # https://publicsuffix.org/list/public_suffix_list.dat
        if is_py_2:
            # for python 2.x
            from httplib import HTTPSConnection
            from StringIO import StringIO
        else:
            # for python 3.x
            from http.client import HTTPSConnection
            from io import StringIO
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

from httplib import HTTPSConnection


def read_suffix_list(content):
    '''
    Read and parse suffix list.
    '''
    # remove comment & blank line
    suffix_list = [line.lower().strip().decode('utf-8')
                   for line in contents
                   if not line.startswith('//') and line.strip()]

    # find idna decodable suffixs
    idna_encoded_suffix_list = []
    for suffix in suffix_list:
        try:
            encoded = suffix.encode('idna')
            if suffix != encoded:
                idna_encoded_suffix_list.append(encoded)
        except Exception:
            pass

    idna_encoded_suffix_list.sort()
    # extend idna encoded suffix_list
    suffix_list.extend(idna_encoded_suffix_list)

    suffix_list.sort()

    return suffix_list


def write_suffix_py(o, suffix_list):
    '''
    Write suffix list as python source.
    '''
    o.write('# -*- coding: utf-8 -*-\n\n')

    def write(var_begin, suffix_lst, end, line_acc, process, process_elem):
        first_line_max_length = 79 - len(var_begin)
        line_max_length = first_line_max_length
        one_line_max_length = first_line_max_length
        count, tmp, indent = 0, [], 0
        o.write(var_begin)
        for suffix in suffix_lst:
            processed_elem, length = process_elem(suffix)
            length += len(processed_elem)
            if count + len(processed_elem) + line_acc >= line_max_length:
                o.write((' ' * indent + process(tmp, indent == 0))
                        .encode('utf-8'))
                o.write('\n')
                tmp, count, indent = [], 0, len(var_begin)
                line_max_length = one_line_max_length
            tmp.append(processed_elem)
            count += length
        if tmp:
            o.write((' ' * indent +
                     process(tmp, indent == 0)).encode('utf-8'))
        o.write(end)

    # Write suffixes list.
    #
    # write('SUFFIXES = [', suffix_list, ' ]', 1,
    #       lambda x, f: u', '.join(x) + u',',
    #       lambda x: (u'u"%s"' % x, 2))

    # o.write('\n\n')

    # write public suffixes Regular Expression.
    suffix_list = map(lambda x: x.replace('.', '\\.')
                      .replace('*', '[^.]+').replace('!', ''),
                      suffix_list)
    suffix_list.sort()
    suffix_list.reverse()
    write('SUFFIXES_RE = (', suffix_list, ')', 3,
          lambda x, f: (u'u"%s"' if f else u'u"|%s"') % u'|'.join(x),
          lambda x: (x, 1))
    o.write('\n')

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
        connection = HTTPSConnection('publicsuffix.org')
        connection.request('GET', '/list/public_suffix_list.dat')
        response = connection.getresponse()

        import StringIO
        contents = StringIO.StringIO(response.read())
    else:
        contents = open(args.filename, 'r')

    suffix_list = read_suffix_list(contents)
    contents.close()

    if args.output == '-':
        # use stdout
        from sys import stdout
        o = stdout
    else:
        o = open(args.output, 'w')

    write_suffix_py(o, suffix_list)
    o.close()

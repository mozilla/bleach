#!/usr/bin/env python

import webbrowser


TEST_BROWSERS = set([
    # 'mozilla',
    'firefox',
    # 'netscape',
    # 'galeon',
    # 'epiphany',
    # 'skipstone',
    # 'kfmclient',
    # 'konqueror',
    # 'kfm',
    # 'mosaic',
    # 'opera',
    # 'grail',
    # 'links',
    # 'elinks',
    # 'lynx',
    # 'w3m',
    'windows-default',
    # 'macosx',
    'safari',
    # 'google-chrome',
    'chrome',
    # 'chromium',
    # 'chromium-browser',
])
REGISTERED_BROWSERS = set(webbrowser._browsers.keys())


if __name__ == '__main__':
    for b in TEST_BROWSERS & REGISTERED_BROWSERS:
        webbrowser.get(b).open_new_tab('http://localhost:8080')

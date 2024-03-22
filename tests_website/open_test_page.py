#!/usr/bin/env python

import webbrowser


TEST_BROWSERS = {
    # 'mozilla',
    "firefox",
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
    "windows-default",
    # 'macosx',
    "safari",
    # 'google-chrome',
    "chrome",
    # 'chromium',
    # 'chromium-browser',
}


if __name__ == "__main__":
    for browser_name in TEST_BROWSERS:
        try:
            browser = webbrowser.get(browser_name)
            browser.open_new_tab("http://localhost:8080")
        except Exception as error:
            print(f"error getting test browser {browser_name}: {error}")

from bleach import (Bleach, ALLOWED_TAGS, ALLOWED_ATTRIBUTES,
                    ALLOWED_STYLES, identity)


__version__ = '0.5.0'

__all__ = ['Bleach', 'clean', 'linkify']

_my_bleach = Bleach()


def clean(text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
          styles=ALLOWED_STYLES, strip=False, strip_comments=False):
    return _my_bleach.clean(text, tags=tags, attributes=attributes,
                            styles=styles, strip=strip,
                            strip_comments=strip_comments)


def linkify(text, nofollow=True, nofollow_relative=False,
            filter_url=identity, filter_text=identity):
    return _my_bleach.linkify(text, nofollow=nofollow,
                              nofollow_relative=nofollow_relative,
                              filter_url=filter_url, filter_text=filter_text)

"""A set of basic callbacks for bleach.linkify."""

import re

nofollow_re = re.compile(r'^.*?(\b|\s)(nofollow)(\b|(\s.*))?$', re.U | re.I)


def nofollow(attrs, new=False):
    if attrs['href'].startswith('mailto:'):
        return attrs
    rel = attrs.get('rel', False)
    if rel:
        if not nofollow_re.match(rel):
            attrs['rel'] = u' '.join([rel, u'nofollow'])
    else:
        attrs['rel'] = u'nofollow'

    return attrs


def target_blank(attrs, new=False):
    if attrs['href'].startswith('mailto:'):
        return attrs
    attrs['target'] = '_blank'
    return attrs

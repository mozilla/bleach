"""A set of basic callbacks for bleach.linkify."""
import six
import re

nfre = re.compile(r'^.*?(\b|\s)(nofollow)(\b|(\s.*))?$', re.U|re.I)

def nofollow(attrs, new=False):
    if attrs['href'].startswith('mailto:'):
        return attrs
    rel = attrs.get('rel', six.u(''))
    if rel :
        if not nfre.match(rel):
            attrs['rel'] = six.u(' ').join([rel, six.u('nofollow')])
    else : 
        attrs['rel'] = six.u('nofollow')
    return attrs


def target_blank(attrs, new=False):
    if attrs['href'].startswith('mailto:'):
        return attrs
    attrs['target'] = six.u('_blank')
    return attrs

from typing import Optional
from pyshorteners import Shortener, exceptions
from shorty.validators import Provider
import functools
import os

# creating shortener object
# contains api interface with different platforms
shortener = Shortener(api_key=os.environ.get('API-KEY'))


@functools.lru_cache(maxsize=1024)
def get_short_link(url: str, provider: Optional[str]) -> tuple[str, bool]:
    """
    Compresses the link according to provider argument.
    If provider is not specified trying to check everyone to success
    :param url: full link to source
    :param provider: provider to compress link
    :return: compressed url and error handler
    """
    if provider:
        # return values according to provider
        if provider == Provider.bitly:
            return get_from_bit(url)
        if provider == Provider.tinyurl:
            return get_from_tinyurl(url)
    else:
        # checking 'bit.ly'
        short_link, error = get_from_bit(url)
        if not error:
            return short_link, error
        # checking 'tinyurl.com'
        short_link, error = get_from_tinyurl(url)
        if not error:
            return short_link, error
    # if not returned earlier returns empty url with error flag
    return '', True


def get_from_bit(url: str) -> tuple[str, bool]:
    """
    compress link via bit.ly
    :param url: long link
    :return: compressed url and error handler
    """
    try:
        # shortening the link
        res = shortener.bitly.short(url)
        return res, False
    except Exception:
        # exception connected with wrong api_key or something connected with bit.ly server
        return '', True


def get_from_tinyurl(url: str) -> tuple[str, bool]:
    """
    compress link via tinyurl.com
    :param url: long link
    :return: compressed url and error handler
    """
    try:
        # shortening the link
        res = shortener.tinyurl.short(url)
        return res, False
    except Exception:
        # exception connected with wrong data in url
        return '', True

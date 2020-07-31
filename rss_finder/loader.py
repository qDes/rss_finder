import asyncio
import copy
import signal
from contextlib import contextmanager
from async_timeout import timeout

import aiohttp
import requests
import concurrent
from . import exceptions


class TimeoutException(Exception): pass


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException('Timed out!')
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


class Loader:
    requests_options_default = {
        'allow_redirects': True,
        'timeout': (10, 30),
        'headers': {},
        'verify': False,
    }

    default_timeout = 30

    def __init__(self, requests_options=None, timeout=None):
        self.requests_options = copy.deepcopy(self.requests_options_default)
        if not timeout:
            timeout = self.default_timeout
        self.timeout = timeout
        if requests_options and isinstance(requests_options, dict):
            self.requests_options.update(requests_options)

    async def fetch(self, url: str) -> requests.Response:
        try:
            async with timeout(self.timeout):
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, ssl=False) as response:
                        status = response.status
                        text = await response.text()
                        return text, status
            '''
            with time_limit(self.timeout):
                return requests.get(url, params=self.requests_options)
            '''
        except (requests.RequestException, ConnectionError,
                UnicodeDecodeError, TimeoutException,
                asyncio.TimeoutError, UnicodeError,
                aiohttp.client_exceptions.ClientOSError,
                concurrent.futures._base.CancelledError,
                ValuerError) as e:
            raise exceptions.RequestException('Error load url "{0}"'.format(url)) from e

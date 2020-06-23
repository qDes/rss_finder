RSS feed finder
===========================

Overview
---------
Finds RSS feed URLS for a given url.

Features
-----
1. Search rss urls based on <link> tag
2. Search rss urls based on <a> tag (href attribute contains rss labels)
3. Check standard rss urls for multiple CMS

Installation
-----
Install via pip:
```bash 
pip install -U git+https://github.com/qDes/rss_finder.git#egg=rss_finder
```

Usage


Usage in code:\
```python
import asyncio

from rss_finder.finder import RssFinder


async def main():
    finder = RssFinder()

    res = await finder.search('tadviser.ru/')
    print(res)


if __name__ == "__main__":
    asyncio.run(main())
```

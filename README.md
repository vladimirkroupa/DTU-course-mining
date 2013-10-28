DTU course mining project with Python
==============

Running the scraper:
--------------
    cd scraper;
    scrapy crawl CourseSpider -o [output.json] -t json


Running unit tests:
--------------
from the project root dir:

    python -m unittest discover


List of libraries to install:
--------------
- python-scrapy
- mock

Complete list of dependencies:
--------------
CherryPy==3.2.4
Mako==0.9.0
Markdown==2.3.1
MarkupSafe==0.18
Scrapy==0.18.2
Twisted==13.1.0
argparse==1.2.1
distribute==0.6.34
lxml==3.2.3
mock==1.0.1
pdoc==0.1.8
pyOpenSSL==0.13.1
queuelib==1.0
w3lib==1.3
wsgiref==0.1.2
zope.interface==4.0.5


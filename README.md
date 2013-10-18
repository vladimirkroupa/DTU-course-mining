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

import os

from scrapy.http import HtmlResponse, Request

def fake_response_from_file(file_path, url=None):
    """
    Create a Scrapy fake HTTP response from a HTML file
    @param file_path: TODO
    @param url: The URL of the response.
    returns: A scrapy HTTP response which can be used for unittesting.
    """
    if not url:
        url = 'http://www.example.com'

    request = Request(url=url)

    file_content = open(file_path, 'r').read()

    response = HtmlResponse(
        url=url,
        request=request,
        body=file_content,
        encoding = 'utf-8')
    return response
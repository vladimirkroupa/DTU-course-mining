from urllib import urlencode
from urlparse import parse_qs, urlsplit, urlunsplit

class PageStructureException(Exception):
    pass


def select_single(selector, xpath):
    return select(selector, xpath, expected = 1)[0]

def select(selector, xpath, expected):
    result = selector.select(xpath)
    if expected is not None and len(result) != expected:
        msg = "Expected {0} result(s), got {1}. XPath expression: {2} Selector content: {3}".format(expected, len(result), xpath, selector.extract().encode('utf-8'))
        raise PageStructureException(msg)
    return result

def check_len(list, item_count):
    if len(list) != item_count:
        raise PageStructureException("Expected {0} element(s), got: {1}".format(item_count, len(list)))
    return list

def single_elem(list):
    check_len(list, 1)
    return list[0]

def set_url_param(url, param_name, param_value):
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)

    query_params[param_name] = [param_value]
    new_query_string = urlencode(query_params, doseq=True)

    return urlunsplit((scheme, netloc, path, new_query_string, fragment))
import unittest
from util.scrapy_utils import set_url_param

class ScrapyUtilsTest(unittest.TestCase):

    def test_set_url_param(self):
        url = 'http://www.kurser.dtu.dk/finalevaluationresults/Default.aspx?coursecode=11B12&schemaInstanceID=68298'
        expected_url = 'http://www.kurser.dtu.dk/finalevaluationresults/Default.aspx?language=en-GB&coursecode=11B12&schemaInstanceID=68298'
        actual_url = set_url_param(url, 'language', 'en-GB')
        self.assertEqual(expected_url, actual_url)
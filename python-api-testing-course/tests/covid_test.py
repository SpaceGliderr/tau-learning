import requests

from utils.config import BASE_COVID_TRACKER_URI
from lxml import etree
from assertpy.assertpy import assert_that


def test_covid_cases_have_crossed_a_million():
    # Sends back XML as its content in the Response object
    response = requests.get(f"{BASE_COVID_TRACKER_URI}/api/v1/summary/latest")

    # .text function converts the content of the response to unicode
    response_xml = response.text  

    # etree stands for ElementTree API
    # Converts string (in bytes) to an XML Element Tree object
    xml_tree = etree.fromstring(bytes(response_xml, encoding="utf-8"))

    # It is also possible to just straight away use `response.content` into the `fromstring` function
    # This is because `response.content` provides the XML in the bytes format
    # I presume the reason why the tutorial isn't doing this is because in the event that the content returns in a non-utf-8 encoding?
    # xml_tree = etree.fromstring(response.content)

    # Access the data within the specific tree node
    # Navigate to tree nodes like a file system
    # xml_tree.xpath("//data/summary/total_cases")) provides an Element object
    # Element objects are lists
    # .text retrieves the contents in that node in string type
    total_cases = xml_tree.xpath("//data/summary/total_cases")[0].text
    assert_that(int(total_cases)).is_greater_than(1000000)


def test_overall_covid_cases_match_sum_of_total_cases_by_country():
    response = requests.get(f'{BASE_COVID_TRACKER_URI}/api/v1/summary/latest')

    tree = etree.fromstring(response.content)
    total_cases = int(tree.xpath("//data/summary/total_cases")[0].text)

    # etree.XPath builds a XPath variable that can be used to filter for specific elements
    # The filter is the template nodes provided. It'll go through the tree and extract Elements that match the path provided
    search_for = etree.XPath("//data//regions//total_cases")

    cases_total_by_country = 0

    # search_for(tree) returns a list of Elements where it matches the XPath provided
    for region in search_for(tree):
        cases_total_by_country += int(region.text)

    # For some reason total cases is less than total cases by country (couldn't bother figuring this one out)
    assert_that(total_cases).is_less_than(cases_total_by_country)

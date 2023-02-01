"""Module with core functionality for web scraping"""

import json
import time

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

from web_scraping.zap_imoveis.scraper.property import ZapProperty
import web_scraping.zap_imoveis.scraper.utils as utils


__all__ = [
    # Main search function.
    "search",
]

# Default user agent, unless instructed by the user to change it:
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"


def get_page_content(url):

    """Function to get page content given url"""

    request = Request(url)
    request.add_header("User-Agent", USER_AGENT)

    response = urlopen(request)

    return response


def get_listings(soup):

    """Function used to retrieve all property listings using BeautifulSoup"""

    page_data_string = soup.find(
        lambda tag: tag.name == "script"
        and isinstance(tag.string, str)
        and tag.string.startswith("window")
    )

    json_string = page_data_string.string.replace(
        "window.__INITIAL_STATE__=", ""
    ).replace(
        ";(function(){var s;(s=document.currentScript||document.scripts[document.scripts.length-1]).parentNode.removeChild(s);}());",
        "",
    )

    return json.loads(json_string)["results"]["listings"]


def get_zap_property(listing):

    # Loading empty item:
    item = ZapProperty()

    print(listing["listing"])

    # General:
    item.id = listing["listing"]["id"]
    item.short_description = listing["link"]["name"]
    item.title = listing["listing"]["title"]
    item.description = listing["listing"]["description"]
    item.unit_types = listing["listing"]["unitTypes"]
    item.created_at = listing["listing"]["createdAt"]
    item.updated_at = listing["listing"]["updatedAt"]
    item.link = listing["link"]["href"]
    item.status = listing["listing"]["status"]
    item.images = listing["listing"]["images"]

    # Address:
    item.address_country = listing["listing"]["address"]["country"]
    item.address_city = listing["listing"]["address"]["city"]
    item.address_zone = listing["listing"]["address"]["zone"]
    item.address_district = listing["listing"]["address"]["district"]
    item.address_neighborhood = listing["listing"]["address"]["neighborhood"]
    item.address_street = listing["listing"]["address"]["street"]
    item.address_street_number = listing["listing"]["address"]["streetNumber"]
    item.address_zip_code = listing["listing"]["address"]["zipCode"]
    item.address_level = listing["listing"]["address"]["level"]
    item.address_longitude = listing["listing"]["address"]["point"]["lon"]
    item.address_latitude = listing["listing"]["address"]["point"]["lat"]

    # Pricing:
    item.pricing_business_type = listing["listing"]["pricingInfos"][0]["businessType"]
    item.pricing_period = listing["listing"]["pricingInfos"][0]["rentalInfo"]["period"]
    item.pricing_rent = listing["listing"]["pricingInfos"][0]["price"]
    item.pricing_monthly_condo_fee = listing["listing"]["pricingInfos"][0][
        "monthlyCondoFee"
    ]
    item.pricing_yearly_iptu = listing["listing"]["pricingInfos"][0]["yearlyIptu"]
    item.pricing_monthly_total = listing["listing"]["pricingInfos"][0]["rentalInfo"][
        "monthlyRentalTotalPrice"
    ]

    # Quantitative features:
    item.total_area_m2 = listing["listing"]["usableAreas"]
    item.num_bedrooms = listing["listing"]["bedrooms"]
    item.num_bathrooms = listing["listing"]["bathrooms"]
    item.parking_spaces = listing["listing"]["parkingSpaces"]
    item.floors = listing["listing"]["floors"]
    item.unit_floor = listing["listing"]["unitFloor"]

    # Qualitative_features:
    item.listing_type = listing["listing"]["listingType"]
    item.amenities = listing["listing"]["amenities"]
    item.points_of_interest = listing["listing"]["address"]["poisList"]

    """
    item.link = listing["link"]["href"]
    item.price = (
        listing["listing"]["pricingInfos"][0].get("price", None)
        if len(listing["listing"]["pricingInfos"]) > 0
        else 0
    )
    item.condo_fee = (
        listing["listing"]["pricingInfos"][0].get("monthlyCondoFee", None)
        if len(listing["listing"]["pricingInfos"]) > 0
        else 0
    )
    item.bedrooms = (
        listing["listing"]["bedrooms"][0]
        if len(listing["listing"]["bedrooms"]) > 0
        else 0
    )
    item.bathrooms = (
        listing["listing"]["bathrooms"][0]
        if len(listing["listing"]["bathrooms"]) > 0
        else 0
    )
    item.vacancies = (
        listing["listing"]["parkingSpaces"][0]
        if len(listing["listing"]["parkingSpaces"]) > 0
        else 0
    )
    item.total_area_m2 = (
        listing["listing"]["usableAreas"][0]
        if len(listing["listing"]["usableAreas"]) > 0
        else 0
    )
    item.address = (
        (
            listing["link"]["data"]["street"]
            + ", "
            + listing["link"]["data"]["neighborhood"]
        )
        .strip(",")
        .strip()
    )
    item.description = listing["listing"]["title"]
    """

    return item


def search_zap_imoveis(
    str_location,
    num_pages=1,
    action="rent",
    property_type="apartment",
    dictionary_out=False,
    time_to_wait=0,
):

    # Initializing variables:
    page = 1
    properties = []

    # Converting inputs to url search parameters:
    action = utils.convert_action(action)
    property_type = utils.convert_property_type(property_type)

    while page <= num_pages:

        # Composing url given parameters:
        url_search = "https://www.zapimoveis.com.br/"
        url_search += f"{action}/"
        url_search += f"{property_type}/"
        url_search += f"{str_location}/"
        url_search += f"?pagina={page}"

        print(url_search)

        # Using BeautifulSoup to parse page content:
        html = get_page_content(url_search)
        soup = BeautifulSoup(html, "html.parser")

        # Retrieving properties from html:
        listings = get_listings(soup)

        for listing in listings:
            if "type" not in listing or listing["type"] != "nearby":
                property_data = get_zap_property(listing)
                properties.append(property_data)

        # Incrementing page and sleeping until content loads:
        page += 1
        time.sleep(time_to_wait)

    # Returning data as dictionary, if requested:
    if dictionary_out:
        return utils.convert_dict(properties)

    return properties

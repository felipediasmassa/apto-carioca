"""Module with core functionality for web scraping"""

import json
import time
import math

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

from web_scraping.zap_imoveis.search_all_apts.scraper.property import ZapProperty
from web_scraping.zap_imoveis.search_all_apts.scraper import utils


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

    # Preprocessing:
    listing_key = listing.get("listing", {})
    link_key = listing.get("link", {})
    address = listing_key.get("address", {})
    address_coordinates = address.get("point", {})
    pricing_infos = listing_key.get("pricingInfos", {})
    if pricing_infos:
        pricing_infos = pricing_infos[0]
        rental_info = pricing_infos.get("rentalInfo", {})
    else:
        rental_info = {}

    # General:
    item.id = listing_key.get("id")
    item.short_description = link_key.get("name")
    item.title = listing_key.get("title")
    item.description = listing_key.get("description")
    item.unit_types = listing_key.get("unitTypes")
    item.created_at = listing_key.get("createdAt")
    item.updated_at = listing_key.get("updatedAt")
    item.link = link_key.get("href")
    item.status = listing_key.get("status")
    item.images = listing_key.get("images")

    # Address:
    item.address_country = address.get("country")
    item.address_city = address.get("city")
    item.address_zone = address.get("zone")
    item.address_district = address.get("district")
    item.address_neighborhood = address.get("neighborhood")
    item.address_street = address.get("street")
    item.address_street_number = address.get("streetNumber")
    item.address_zip_code = address.get("zipCode")
    item.address_level = address.get("level")
    item.address_longitude = address_coordinates.get("lon")
    item.address_latitude = address_coordinates.get("lat")

    # Pricing:
    item.pricing_business_type = pricing_infos.get("businessType")
    item.pricing_period = rental_info.get("period")
    item.pricing_rent = pricing_infos.get("price")
    item.pricing_monthly_condo_fee = pricing_infos.get("monthlyCondoFee")
    item.pricing_yearly_iptu = pricing_infos.get("yearlyIptu")
    item.pricing_monthly_total = rental_info.get("monthlyRentalTotalPrice")

    # Quantitative features:
    item.total_area_m2 = listing_key.get("usableAreas")
    item.num_bedrooms = listing_key.get("bedrooms")
    item.num_bathrooms = listing_key.get("bathrooms")
    item.parking_spaces = listing_key.get("parkingSpaces")
    item.floors = listing_key.get("floors")
    item.unit_floor = listing_key.get("unitFloor")

    # Qualitative_features:
    item.listing_type = listing_key.get("listingType")
    item.amenities = listing_key.get("amenities")
    item.points_of_interest = address.get("poisList")

    return item


def search_zap_imoveis(
    str_location,
    num_pages=None,
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

    old_len, new_len = -1, 0  # initializing old_len with -1 to start while loop

    if not num_pages:
        num_pages = math.inf  # setting number of pages to infinity if not passed

    while page <= num_pages and old_len < new_len:

        # Calculating length of retrieved properties list at start of iteration:
        old_len = len(properties)

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

        # Calculating length of retrieved properties list at end of iteration:
        new_len = len(properties)

    # Returning data as dictionary, if requested:
    if dictionary_out:
        return utils.convert_dict(properties)

    return properties

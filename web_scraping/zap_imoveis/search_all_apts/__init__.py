"""Module with functions to scrape data from Zap Imóveis based on search parameters"""

import os
import time

import pandas as pd

import pycep_correios as cep
from geopy.geocoders import Nominatim

import web_scraping.zap_imoveis.search_all_apts.scraper as zap


URL_START = "https://www.zapimoveis.com.br"

STATE, CITY, ZONE, DISTRICT = "rj", "rio-de-janeiro", "zona-sul", "botafogo"

NUM_PAGES = None
ACTION = "rent"  # others = "buy", "release"
PROPERTY_TYPE = "apartment"  # others = "property", "house"

GEOLOCATOR = Nominatim(user_agent="webscraper")


def search_properties(
    district: str,
    zone: str,
    city: str = "rio-de-janeiro",
    state: str = "rj",
    num_pages=None,
    action: str = "rent",
    property_type: str = "apartment",
    url_start: str = "https://www.zapimoveis.com.br",
    dictionary_out: bool = False,
):

    """"""

    # Preprocessing parameters:
    str_location = get_location_string(district, zone, city, state)

    # Retrieving all properties objects from search:
    properties = zap.search_zap_imoveis(
        str_location,
        num_pages=num_pages,
        action=action,
        property_type=property_type,
        dictionary_out=dictionary_out,
    )

    properties_dict = [property.__dict__ for property in properties]

    df_properties = pd.DataFrame(properties_dict)

    df_properties["full_link"] = url_start + df_properties["link"]

    # df_properties["lat lon"] = df_properties["address_zip_code"].apply(
    #    get_coordinates_from_address
    # )
    # print(df_properties["lat lon"])

    df_properties.to_excel("output.xlsx")

    df_properties.to_json(
        os.path.join(os.path.dirname(__file__), "df_properties.json"), orient="records"
    )

    return properties_dict


def get_location_string(district, zone, city, state):

    """Function to compose location string"""

    str_location = f"{state}+{city}+{zone}+{district}"

    return str_location


def get_coordinates_from_address(zip_code):

    """"""

    #
    address = cep.get_address_from_cep(zip_code)

    street = f"{address['logradouro'][0]}. {address['logradouro'][3:]}"
    district = address["bairro"]
    city = address["cidade"]

    loc = GEOLOCATOR.geocode(f"{street}, {district}-{city}")

    print(loc)

    time.sleep(5)

    if not loc:
        return None

    return loc.latitude, loc.longitude


search_properties(
    district=DISTRICT,
    zone=ZONE,
    city=CITY,
    state=STATE,
    num_pages=NUM_PAGES,
    action=ACTION,
    property_type=PROPERTY_TYPE,
    url_start=URL_START,
)

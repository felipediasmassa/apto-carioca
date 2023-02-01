import pandas as pd
from geopy.geocoders import Nominatim
import web_scraping.zap_imoveis.scraper as zap

URL_START = "https://www.zapimoveis.com.br"

STATE = "rj"
CITY = "rio-de-janeiro"
ZONE = "zona-sul"
DISTRICT = "botafogo"

NUM_PAGES = 5
ACTION = "rent"  # others = "buy", "release"
PROPERTY_TYPE = "apartment"  # others = "property", "house"

geolocator = Nominatim(user_agent="geolocalização")


def search_properties(
    district: str,
    zone: str,
    city: str = "rio-de-janeiro",
    state: str = "rj",
    num_pages: int = 5,
    action: str = "rent",
    property_type: str = "apartment",
    url_start: str = "https://www.zapimoveis.com.br",
):

    # Preprocessing parameters:
    str_location = get_location_string(district, zone, city, state)

    # Retrieving all properties objects from search:
    properties = zap.search_zap_imoveis(
        str_location,
        num_pages=num_pages,
        action=action,
        property_type=property_type,
    )

    properties_dict = [property.__dict__ for property in properties]

    df_properties = pd.DataFrame(properties_dict)
    print(df_properties)

    df_properties["full_link"] = url_start + df_properties["link"]

    df_properties.to_excel("output.xlsx")

    return properties_dict


def get_location_string(district, zone, city, state):

    """Function to compose location string"""

    str_location = f"{state}+{city}+{zone}+{district}"

    return str_location


def get_coordinates_from_address():

    location = geolocator.geocode(
        "Rua Henrique Portugal 107, São Francisco, Niterói, RJ, Brasil - 24360-080"
    )
    print(location)

    return


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

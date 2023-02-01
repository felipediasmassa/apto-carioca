import pandas as pd
import zapimoveis_scraper as zap

URL_START = "https://www.zapimoveis.com.br"

STATE = "rj"
CITY = "rio-de-janeiro"
ZONE = "zona-sul"
DISTRICT = "botafogo"

NUM_PAGES = 5
ACTION = "rent"  # others = "buy", "release"
PROPERTY_TYPE = "apartment"  # others = "property", "house"


def search_apts(
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
    action = map_action(action)
    property_type = map_property_type(property_type)

    # Retrieving all properties objects from search:
    properties = zap.search(
        str_location,
        num_pages=num_pages,
        acao=action,
        tipo=property_type,
    )

    properties_dict = [property.__dict__ for property in properties]

    df_properties = pd.DataFrame(properties_dict)
    print(df_properties)

    df_properties["full_link"] = url_start + df_properties["link"]

    df_properties.to_excel("output.xlsx")

    return properties_dict


def get_location_string(district, zone, city, state):

    str_location = f"{state}+{city}+{zone}+{district}"

    return str_location


def map_action(action):

    action_map = {
        "buy": "venda",
        "rent": "aluguel",
        "release": "lancamentos",
    }

    action = action_map[action]

    return action


def map_property_type(property_type):

    property_type_map = {
        "property": "imoveis",
        "apartment": "apartamentos",
        "house": "casas",
    }

    property_type = property_type_map[property_type]

    return property_type


search_apts(
    district=DISTRICT,
    zone=ZONE,
    city=CITY,
    state=STATE,
    num_pages=NUM_PAGES,
    action=ACTION,
    property_type=PROPERTY_TYPE,
    url_start=URL_START,
)

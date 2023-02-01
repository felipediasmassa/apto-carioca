"""Module with utility functions used by scraper"""


def convert_dict(property_data):

    """
    Function to convert the data from object to a dictionary
    """

    # Creating dictionary from object:
    property_dict = property_data.__dict__

    return property_dict


def convert_action(action):

    """Function to convert action string to appropriate keyword for search url"""

    action_dict = {
        "buy": "venda",
        "rent": "aluguel",
        "release": "lancamentos",
    }

    return action_dict[action]


def convert_property_type(property_type):

    """Function to convert property type string to appropriate keyword for search url"""

    property_type_dict = {
        "property": "imoveis",
        "apartment": "apartamentos",
        "house": "casas",
    }

    return property_type_dict[property_type]

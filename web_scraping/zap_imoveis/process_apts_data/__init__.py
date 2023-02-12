"""Module with functions to process scraped data to database-friendly datatypes"""

import pandas as pd


JSON_PATH = "web_scraping/zap_imoveis/search_all_apts/df_properties.json"


def process_apts_data(json_path):

    """Function to process apartaments data applying data transformation functions"""

    df_properties = pd.read_json(json_path)

    # General data:
    df_properties["id"] = convert_datatype(df_properties["id"], int)
    df_properties["short_description"] = convert_datatype(
        df_properties["short_description"], str
    )
    df_properties["short_description"] = convert_datatype(
        df_properties["short_description"], str
    )
    df_properties["title"] = convert_datatype(df_properties["title"], str)
    df_properties["description"] = convert_datatype(df_properties["description"], str)
    df_properties["unit_types"] = convert_str_to_list(
        df_properties["unit_types"], dtype_conversion_func=str
    )
    df_properties["created_at"] = convert_datatype(
        df_properties["created_at"], "datetime64[ns, UTC]"
    )
    df_properties["updated_at"] = convert_datatype(
        df_properties["updated_at"], "datetime64[ns, UTC]"
    )
    df_properties["link"] = convert_datatype(df_properties["link"], str)
    df_properties["status"] = convert_datatype(df_properties["status"], str)
    df_properties["images"] = get_image_data(df_properties["images"])

    # Address data:

    # Pricing data:

    # Quantitative features:
    df_properties["total_area_m2"] = convert_str_to_list(
        df_properties["total_area_m2"], dtype_conversion_func=float
    )
    df_properties["num_bedrooms"] = convert_str_to_list(
        df_properties["num_bedrooms"], dtype_conversion_func=int
    )

    # Qualitative features:

    return df_properties


def convert_datatype(series, dtype):

    """Function to convert series datatype"""

    series = series.astype(dtype)

    return series


def convert_str_to_list(series, dtype_conversion_func=None):

    """Function to convert string to list, converting elements to datatype, if passed"""

    series = series.apply(list)

    if dtype_conversion_func:
        series = series.apply(lambda x: [dtype_conversion_func(e) for e in x])

    return series


def get_image_data(series):

    """
    Function to receive image column and convert list of dicts to list of lists, compatible with
    database format
    """

    # Not passing dtype since it will be handled within get_image_data function:
    image_data = convert_str_to_list(series)

    # Converting dictionaries to lists of values:
    image_data = image_data.apply(lambda x: [list(e.values()) for e in x])

    return image_data


process_apts_data(JSON_PATH)

"""Module with functions to process scraped data to database-friendly datatypes"""

import os

import numpy as np
import pandas as pd


JSON_PATH = "web_scraping/zap_imoveis/search_all_apts/df_properties.json"
THIS_DIR = os.path.dirname(__file__)


def process_apts_data(json_path):

    """Function to process apartaments data applying data transformation functions"""

    df_properties = pd.read_json(json_path)

    # General data:
    df_properties["id"] = convert_datatype(df_properties["id"], float)
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
    df_properties["unit_types"] = convert_list_to_dtype(
        df_properties["unit_types"], dtype_conversion_func=str
    )
    df_properties["created_at"] = convert_datatype(
        df_properties["created_at"], "datetime64[ns, UTC]"
    )
    df_properties["created_at"] = convert_date_to_iso(df_properties["created_at"])
    df_properties["updated_at"] = convert_datatype(
        df_properties["updated_at"], "datetime64[ns, UTC]"
    )
    df_properties["updated_at"] = convert_date_to_iso(df_properties["updated_at"])
    df_properties["link"] = convert_datatype(df_properties["link"], str)
    df_properties["status"] = convert_datatype(df_properties["status"], str)
    df_properties["images"] = get_image_data(df_properties["images"])

    # Address data:
    df_properties["address_country"] = convert_datatype(
        df_properties["address_country"], str
    )
    df_properties["address_city"] = convert_datatype(df_properties["address_city"], str)
    df_properties["address_zone"] = convert_datatype(df_properties["address_zone"], str)
    df_properties["address_district"] = convert_datatype(
        df_properties["address_district"], str
    )
    df_properties["address_neighborhood"] = convert_datatype(
        df_properties["address_neighborhood"], str
    )
    df_properties["address_street"] = convert_datatype(
        df_properties["address_street"], str
    )
    df_properties["address_street_number"] = df_properties["address_street_number"]
    df_properties["address_zip_code"] = df_properties["address_zip_code"]
    df_properties["address_level"] = convert_datatype(
        df_properties["address_level"], str
    )
    df_properties["address_longitude"] = convert_datatype(
        df_properties["address_longitude"], float
    )
    df_properties["address_latitude"] = convert_datatype(
        df_properties["address_latitude"], float
    )

    # Pricing data:
    df_properties["pricing_business_type"] = convert_datatype(
        df_properties["pricing_business_type"], str
    )
    df_properties["pricing_period"] = convert_datatype(
        df_properties["pricing_period"], str
    )
    df_properties["pricing_rent"] = convert_datatype(
        df_properties["pricing_rent"], float
    )
    df_properties["pricing_monthly_condo_fee"] = convert_datatype(
        df_properties["pricing_monthly_condo_fee"], float
    )
    df_properties["pricing_yearly_iptu"] = convert_datatype(
        df_properties["pricing_yearly_iptu"], float
    )
    df_properties["pricing_monthly_total"] = convert_datatype(
        df_properties["pricing_monthly_total"], float
    )

    # Quantitative features:
    df_properties["total_area_m2"] = convert_str_to_list(
        df_properties["total_area_m2"], dtype_conversion_func=float
    )
    df_properties["total_area_m2"] = convert_list_to_dtype(
        df_properties["total_area_m2"], dtype_conversion_func=float
    )
    df_properties["num_bedrooms"] = convert_str_to_list(
        df_properties["num_bedrooms"], dtype_conversion_func=int
    )
    df_properties["num_bedrooms"] = convert_list_to_dtype(
        df_properties["num_bedrooms"], dtype_conversion_func=int
    )
    df_properties["num_bathrooms"] = convert_str_to_list(
        df_properties["num_bathrooms"], dtype_conversion_func=int
    )
    df_properties["num_bathrooms"] = convert_list_to_dtype(
        df_properties["num_bathrooms"], dtype_conversion_func=int
    )
    df_properties["parking_spaces"] = convert_str_to_list(
        df_properties["parking_spaces"], dtype_conversion_func=int
    )
    df_properties["parking_spaces"] = convert_list_to_dtype(
        df_properties["parking_spaces"], dtype_conversion_func=int
    )
    df_properties["floors"] = convert_str_to_list(
        df_properties["floors"], dtype_conversion_func=int
    )
    df_properties["floors"] = convert_list_to_dtype(
        df_properties["floors"], dtype_conversion_func=int
    )
    df_properties["unit_floor"] = convert_datatype(df_properties["unit_floor"], int)

    # Qualitative features:
    df_properties["listing_type"] = convert_datatype(df_properties["listing_type"], str)
    df_properties["amenities"] = convert_str_to_list(
        df_properties["amenities"], dtype_conversion_func=str
    )
    df_properties["points_of_interest"] = convert_str_to_list(
        df_properties["points_of_interest"], dtype_conversion_func=str
    )
    df_properties["full_link"] = convert_datatype(df_properties["full_link"], str)

    df_properties.to_json(os.path.join(THIS_DIR, "processed.json"), orient="records")
    df_properties.to_excel(os.path.join(THIS_DIR, "processed.xlsx"))

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


def convert_list_to_dtype(series, dtype_conversion_func=None):

    """Function to receive 1-element list and convert to datatype"""

    count_elements = (series.apply(len) > 1).sum()
    if count_elements > 0:
        raise ValueError(f"Column {series.name} contains more than one element")

    series = series.apply(
        lambda x: dtype_conversion_func(x[0]) if len(x) > 0 else np.nan
    )

    return series


def convert_date_to_iso(series):

    """Function that converts datetimes in np.datetime64 to iso format"""

    return series.apply(lambda x: x.isoformat())


process_apts_data(JSON_PATH)

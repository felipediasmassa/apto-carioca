"""Module defining class to receive property data"""


class ZapProperty:

    """Class to receive property data"""

    # General:
    apt_id = None
    short_description = None
    title = None
    description = None
    unit_types = None
    created_at = None
    updated_at = None
    link = None
    status = None
    images = None

    # Address:
    address_country = None
    address_city = None
    address_zone = None
    address_district = None
    address_neighborhood = None
    address_street = None
    address_street_number = None
    address_zip_code = None
    address_level = None
    address_longitude = None
    address_latitude = None

    # Pricing:
    pricing_business_type = None
    pricing_period = None
    pricing_rent = None
    pricing_monthly_condo_fee = None
    pricing_yearly_iptu = None
    pricing_monthly_total = None

    # Quantitative features:
    total_area_m2 = None
    num_bedrooms = None
    num_bathrooms = None
    parking_spaces = None
    floors = None
    unit_floor = None

    # Qualitative_features:
    listing_type = None
    amenities = None
    points_of_interest = None

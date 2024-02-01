def transform_zipcode(zipcode: str) -> str:
    """
    Transforms a ZIP code to its 5-digit format.

    This function takes a ZIP code, which can be in the standard 5-digit format or
    the extended ZIP+4 format (9 digits with a hyphen). If the ZIP code is in the
    extended format, it trims it to the standard 5-digit format. If the ZIP code is
    already in the 5-digit format, it is returned as is.

    Args:
    zipcode (str): A ZIP code string, which can be either the standard 5-digit
                   format or the extended ZIP+4 format.

    Returns:
    str: The standard 5-digit ZIP code format.

    Examples:
    >>> transform_zipcode("12345-6789")
    '12345'
    >>> transform_zipcode("12345")
    '12345'
    """
    return zipcode.split("-")[0] if "-" in zipcode else zipcode

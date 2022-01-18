class PricingHoursError(Exception):
    """
    An exception being raised when pricing hours don't match working hours.
    """
    pass


class EmptyPriceListError(Exception):
    """
    An exception being raised when price list is empty.
    """
    pass

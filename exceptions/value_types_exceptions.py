class NegativePriceError(Exception):
    """
    An exception being raised when a Price object (initialized or result
    after subtraction) has negative attributes.
    """
    pass


class HoursRangeError(Exception):
    """
    An exception being raised when an HoursRange object's end time attribute
    is earlier than object's begin time attribute.
    """
    pass

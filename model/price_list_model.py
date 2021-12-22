from value_types import Price


class PriceListPosition:
    def __init__(self, service, day, hours_range) -> None:
        self.service = service
        self.day = day
        self.hours_range = hours_range


class PriceListModel:
    def __init__(self) -> None:
        self.pricing = []

    def read_pricing(self):
        pass

    def write_pricing(self):
        pass

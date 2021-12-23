from model.value_types import Price, HoursRange, Services, WeekDay


class PriceListPosition:
    def __init__(
        self, service: Services, day: WeekDay,
        hours_range: HoursRange, price: Price
    ) -> None:

        self.service = Services(service)
        self.day = WeekDay(day)
        self.hours_range = hours_range
        self.price = price

    @staticmethod
    def from_json(json_dict: dict):
        service = json_dict["service"]
        day = json_dict["day"]
        hours_range = HoursRange.from_json(json_dict["hours_range"])
        price = Price.from_json(json_dict["price"])

        return PriceListPosition(service, day, hours_range, price)

    def _data_validation(self, hours_range, price):
        if not isinstance(hours_range, HoursRange):
            raise TypeError("Range of hours must be HoursRange instance")

        if not isinstance(price, Price):
            raise TypeError("Price must be Price instance")


class PriceListModel:
    def __init__(self, working_hours) -> None:
        self._price_list_validation(working_hours)
        self._pricing = []

    def get_pricing(self, service: Services = None) -> list:
        if service is None:
            return self._pricing

        filtered_positions = []

        for position in self._pricing:
            if position.service == service:
                filtered_positions.append(position)

        return filtered_positions

    def _price_list_validation(self, working_hours):
        # 1. Check if pricing hours are the same like working hours
        # 2. Check if pricing hours don't intersect
        pass

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

    def _data_validation(self, hours_range, price):
        if not isinstance(hours_range, HoursRange):
            raise TypeError("Range of hours must be HoursRange instance")

        if not isinstance(price, Price):
            raise TypeError("Price must be Price instance")


class PriceListModel:
    def __init__(self, pool_model) -> None:
        self._price_list_validation(pool_model)
        self._pricing = []

    def get_pricing(self, service: Services = None) -> list:
        if service is None:
            return self._pricing

        filtered_positions = []

        for position in self._pricing:
            if position.service == service:
                filtered_positions.append(position)

        return filtered_positions

    def _price_list_validation(self, pool_model):
        pass

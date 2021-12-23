from exceptions.price_list_exceptions import PricingHoursError
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
    def __init__(self, working_hours: dict, pricing_json: dict) -> None:
        self._pricing = self.read_pricing(pricing_json)
        self._price_list_validation(working_hours)

    def read_pricing(self, pricing_json: dict) -> list:
        # @TODO: Implement method that creates the list of PriceListPosition
        # objects based on a JSON dictionary
        pass

    def get_pricing(self, service: Services = None) -> list:
        if service is None:
            return self._pricing

        filtered_positions = []

        for position in self._pricing:
            if position.service == service:
                filtered_positions.append(position)

        return filtered_positions

    def _price_list_validation(self, working_hours: dict):
        # Working hours is a dict WeekDay -> HoursRange

        # 1. Get the lists of PriceListPosition objects
        # separately for individuals and schools

        ind_pricing = self.get_pricing(Services.INDIVIDUAL)
        school_pricing = self.get_pricing(Services.SWIMMING_SCHOOL)

        # 2. Sort both lists by the begin hour of the PriceListPosition object

        sorted_ind_pricing = sorted(
            ind_pricing, key=lambda price_pos: price_pos.hours_range.begin)
        sorted_school_pricing = sorted(
            school_pricing, key=lambda price_pos: price_pos.hours_range.begin)

        # 3. Initialize dictionaries, that to every day assign connected
        # hour ranges of the pricing (will throw an exception if hours are
        # disconnected or intersect)

        ind_hours = {}
        school_hours = {}

        for day in working_hours:
            ind_hours[day] = sum(
                position.hours_range for position in sorted_ind_pricing)
            school_hours[day] = sum(
                position.hours_range for position in sorted_school_pricing
            )

        # 4. Check if those hours match the working hours

        for day in ind_hours:
            if ind_hours[day] != working_hours[day]:
                raise PricingHoursError(
                    "Pricing hours don't match pool working hours")

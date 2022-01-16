from exceptions.price_list_exceptions import EmptyPriceListError
from exceptions.price_list_exceptions import PricingHoursError
from model.value_types import Price, HoursRange, Services, WeekDay


class PriceListPosition:
    """
    Represents a single position on a price list. Stores information about
    service type, week day, hours range and reservation price per hour.
    """

    def __init__(
        self, service: Services, day: WeekDay,
        hours_range: HoursRange, price: Price
    ) -> None:

        self._data_validation(hours_range, price)

        self.service = Services(service)
        self.day = WeekDay(day)
        self.hours_range = hours_range
        self.price = price

    def __str__(self) -> str:
        day_str = self.day.name.capitalize()

        if self.service == Services.INDIVIDUAL:
            service_str = "individual"
        else:
            service_str = "swimming school"

        price_str = str(self.price)
        hours_str = str(self.hours_range)

        return f"{day_str} ({service_str}, {hours_str}): {price_str} per hour"

    @staticmethod
    def from_json(json_dict: dict):
        """
        Converts a JSON-formatted dictionary to a PriceListPosition object
        and returns it.
        """

        service = Services(json_dict["service"])
        day = WeekDay(json_dict["day"])
        hours_range = HoursRange.from_json(json_dict["hours_range"])
        price = Price.from_json(json_dict["price"])

        return PriceListPosition(service, day, hours_range, price)

    @staticmethod
    def to_json(object) -> dict:
        """
        Converts a PriceListPosition object to a JSON-formatted dictionary
        and returns it.
        """

        json_dict = {
            "service": object.service.value,
            "day": object.day.value,
            "hours_range": HoursRange.to_json(object.hours_range),
            "price": Price.to_json(object.price)
        }

        return json_dict

    def _data_validation(self, hours_range: HoursRange, price: Price) -> None:
        """
        Validates initial data and throws proper exceptions if the given data
        is invalid.
        """

        if not isinstance(hours_range, HoursRange):
            raise TypeError("Range of hours must be HoursRange instance")

        if not isinstance(price, Price):
            raise TypeError("Price must be Price instance")


class PriceListModel:
    """
    Represents the price list. Stores a list of PriceListPosition objects.
    Needs to be initialized using a JSON-formatted list of PriceListPosition
    objects.
    """

    def __init__(
        self, working_hours: dict[WeekDay, HoursRange],
        pricing_json: list
    ) -> None:

        self._pricing = PriceListModel.from_json(pricing_json)
        self._price_list_validation(working_hours)

    def get_pricing(self, service: Services = None) -> list[PriceListPosition]:
        """
        Returns the price list (list of PriceListPosition objects). If service
        is given, returns a list of only these objets with equal service
        attribute (so only the price list for individuals or swimming schools)
        """

        if service is None:
            return self._pricing

        filtered_positions = []

        for position in self._pricing:
            if position.service == Services(service):
                filtered_positions.append(position)

        return filtered_positions

    @staticmethod
    def from_json(pricing_json: list) -> list[PriceListPosition]:
        """
        Converts a list of JSON-formatted PriceListPosition objects
        to the list of PriceListPosition objects and returns it.
        """

        pricing = []

        if not pricing_json:
            raise EmptyPriceListError("Price list cannot be empty.")

        for position in pricing_json:
            pricing.append(PriceListPosition.from_json(position))

        return pricing

    @staticmethod
    def to_json(pricing: list[PriceListPosition]) -> list:
        """
        Converts a list of PriceListPosition objects to the JSON-formatted
        list of PriceListPosition objects.
        """

        json_list = []

        for position in pricing:
            json_list.append(PriceListPosition.to_json(position))

        return json_list

    def _price_list_validation(
        self, working_hours: dict[WeekDay, HoursRange]
    ) -> None:
        """
        Throws an exception if price list doesn't match working hours.
        """

        # 1. Get the lists of PriceListPosition objects
        # separately for individuals and schools

        ind_pricing = self.get_pricing(Services.INDIVIDUAL)
        school_pricing = self.get_pricing(Services.SWIMMING_SCHOOL)

        # 2. Sort both lists first by the WeekDay
        # and then by the begin hour of the PriceListPosition object

        sorted_ind_pricing = sorted(
            ind_pricing,
            key=lambda price_pos: (
                price_pos.day.value, price_pos.hours_range.begin))
        sorted_school_pricing = sorted(
            school_pricing,
            key=lambda price_pos: (
                price_pos.day.value, price_pos.hours_range.begin))

        # 3. Initialize dictionaries, that to every day assign connected
        # hour ranges of the pricing (will throw an exception if hours are
        # disconnected or intersect)

        ind_hours = {}
        school_hours = {}

        for ind_price_pos in sorted_ind_pricing:
            current_hours_range = ind_price_pos.hours_range

            if ind_price_pos.day not in ind_hours:
                ind_hours[ind_price_pos.day] = current_hours_range
            else:
                ind_hours[ind_price_pos.day] += current_hours_range

        for school_price_pos in sorted_school_pricing:
            current_hours_range = school_price_pos.hours_range

            if school_price_pos.day not in school_hours:
                school_hours[school_price_pos.day] = current_hours_range
            else:
                school_hours[school_price_pos.day] += current_hours_range

        # 4. Check if those hours match the working hours

        if ind_hours != working_hours or school_hours != working_hours:
            raise PricingHoursError("Pricing hours don't match working hours.")
